from trip_calculator.models import Trip, UserTrip, Cost, Splited
from django.db.models import Q
from django.db import transaction
from itertools import groupby
from operator import itemgetter
from django.core.cache import cache


class TripController:
    def __init__(self, user_id):
        self.user_id = user_id
        self.trip_details_objects = self.get_trip_details_objects()
        self.trip_info = self.get_trip_info()

    def get_info(self):
        self.trip_details_objects = self.get_trip_details_objects()
        self.trip_info = self.get_trip_info()

        return self.trip_info

    def new_trip(self, name, start, end, description, squad):
        with transaction.atomic():
            new_trip = Trip(name=name, start=start, end=end, description=description, trip_owner_id=self.user_id)
            new_trip.save()
            user_trips = [UserTrip(trip=new_trip, user_id=user_id) for user_id in squad]
            UserTrip.objects.bulk_create(user_trips)
            self.trip_details_objects = self.get_trip_details_objects()

    def get_trip_details_objects(self):
        return Trip.objects.filter(
            Q(trip_owner__user_id=self.user_id) |
            Q(usertrip__user__user_id=self.user_id)
        ).distinct().prefetch_related('cost_set', 'cost_set__splited_set', 'usertrip_set__user')

    def find_trip(self, trip_id):
        for trip in self.trip_details_objects:
            if trip.trip_id == trip_id:
                return trip
        return None

    def update_trip_details(self, trip_id, **kwargs):
        trip = Trip.objects.get(pk= trip_id)

        if trip and trip.trip_owner_id == self.user_id:
            fields_to_update = {
                'name': kwargs.get('name'),
                'description': kwargs.get('description'),
                'delete': kwargs.get('delete')
            }

            for field, value in fields_to_update.items():
                if value != None:
                    if field == 'delete':
                        trip.delete()
                    else:
                        setattr(trip, field, value)
                        trip.save()
            self.get_info()

    def get_trip_info(self):
        trip_details = []

        for trip in self.trip_details_objects:
            trip_info = {
                'trip_id': trip.trip_id, 'name': trip.name, 'start': trip.start, 'end': trip.end,
                'description': trip.description,
                'owner': trip.trip_owner.user_id == self.user_id,
                'squad': [{'user_id': user_trip.user.user_id, 'firstname': user_trip.user.firstname}
                          for user_trip in trip.usertrip_set.all()],
                'costs': {'own_cost': 0, 'costs': [], 'unpaid_users': []}
            }

            for cost in trip.cost_set.all():
                splited_list = list(cost.splited_set.all())
                payed_was_you = cost.payer.user_id == self.user_id
                user_in_splited = any(splited.user.user_id == self.user_id for splited in splited_list)
                if user_in_splited or payed_was_you:
                    number_of_splited = len(splited_list)
                    unit_cost = float(round(cost.value / number_of_splited if number_of_splited > 0 else 0, 2))
                    unpaid_users = [splited.user for splited in splited_list if not splited.payment]
                    trip_info['costs']['own_cost'] += unit_cost if user_in_splited else 0
                    to_return = unit_cost * len(unpaid_users) if payed_was_you else unit_cost

                    cost_info = {
                        'cost_id': cost.cost_id, 'cost_name': cost.cost_name, 'value': float(cost.value),
                        'unit_cost': unit_cost,
                        'payer': {'user_id': cost.payer.user_id, 'firstname': cost.payer.firstname,
                                  'lastname': cost.payer.lastname,
                                  'was_you':payed_was_you },
                        'splited': [{'user_id': splited.user.user_id, 'payment': splited.payment,
                                     'firstname': splited.user.firstname, 'lastname': splited.user.lastname}
                                    for splited in splited_list],

                        'to_return':round(float(to_return),2)
                    }

                    unpaid = [{'user_id': user.user_id, 'related_id': cost.payer.user_id,
                               'unit_cost': unit_cost if payed_was_you else unit_cost * -1}
                              for user in unpaid_users]

                    trip_info['costs']['costs'].append(cost_info)
                    trip_info['costs']['unpaid_users'].extend(unpaid)

            overall_data = self.prepare_overall_data(trip_info['costs']['unpaid_users'])
            extended_overall_data = self.extend_prepare_overall_data(overall_data, trip.usertrip_set.all())

            trip_info['costs']['unpaid_users'] = extended_overall_data

            trip_details.append(trip_info)
        return trip_details

    def prepare_overall_data(self, unpaid_list):
        if unpaid_list:
            for item in unpaid_list:
                if item['related_id'] == self.user_id:
                    item['user_id'], item['related_id'] = item['related_id'], item['user_id']

            only_for_user = list(
                filter(lambda unpaid: unpaid['user_id'] == self.user_id or unpaid['related_id'] == self.user_id,
                       unpaid_list))
            only_for_user.sort(key=itemgetter('user_id', 'related_id'))

            reduce_only_for_user = [
                {'user_id': key[0],'related_id': key[1],
                 'unit_cost': round(sum(item['unit_cost'] for item in group), 2)}
                for key, group in groupby(only_for_user, key=lambda x: (x['user_id'], x['related_id']))
            ]

            for item in reduce_only_for_user:
                unit_cost = item['unit_cost']
                item['related_user_return'] = unit_cost > 0
                item['unit_cost'] = abs(unit_cost)
            return reduce_only_for_user

    def extend_prepare_overall_data(self, overall_data, data):
        if overall_data:
            for data in data:
                for related in overall_data:
                    if related['related_id'] == data.user_id:
                        related['related_firstname'] = data.user.firstname
                        related['related_lastname'] = data.user.lastname
            return overall_data


class CostController(TripController):
    def add_cost(self, trip_id, name, value, split_user_ids):
        with transaction.atomic():
            new_cost = Cost(trip_id=trip_id, payer_id=self.user_id, cost_name=name, value=value)
            new_cost.save()
            splits = [Splited(cost=new_cost, user_id=user_id, payment=(self.user_id == user_id)) for user_id in
                      split_user_ids]
            Splited.objects.bulk_create(splits)

    def find_cost(self, cost_id):
        for trip in self.trip_details_objects:
            cost = next((cost for cost in trip.cost_set.all() if cost.cost_id == cost_id), None)
            if cost:
                return cost
        return None

    def get_splited_info(self, cost_id):
        cost = self.find_cost(cost_id)
        if cost:
            return list(cost.splited_set.all())
        else:
            return None

    def update_cost_details(self, cost_id, **kwargs):
        cost = Cost.objects.get(cost_id=cost_id)
        splited = Splited.objects.filter(cost_id=cost_id)

        if (cost or splited)and cost.payer_id == self.user_id:
            cost_to_update = {
                'cost_name': kwargs.get('cost_name'),
                'value': kwargs.get('value'),
                'payment': kwargs.get('payment'),
                'delete': kwargs.get('delete')
            }

            for field, value in cost_to_update.items():
                if value != None:
                    if field == 'delete':
                        cost.delete()

                    elif field == 'payment':
                        split_user_id = kwargs.get('split_user_id')
                        split = next(split for split in splited if split.user_id == int(split_user_id))
                        split.payment = value
                        split.save()
                    else:
                        setattr(cost, field, value)
                        cost.save()
            self.get_info()


def get_user_TripController(user_id):
    cache_key = f"TripController_{user_id}"
    service = cache.get(cache_key)

    if not service:
        service = TripController(user_id)
        cache.set(cache_key, service, timeout=60 * 30)

    return service

def get_user_CostController(user_id):
    cache_key = f"CostController_{user_id}"
    service = cache.get(cache_key)

    if not service:
        service = CostController(user_id)
        cache.set(cache_key, service, timeout=60 * 30)

    return service
