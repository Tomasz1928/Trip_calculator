from trip_calculator.models import Trip, UserTrip, Cost, Splited
from django.db.models import Q
from django.db import transaction


class TripController:
    def __init__(self, user_id):
        self.user_id = user_id
        self.trip_details_objects = self.get_trip_details_objects()
        self.trip_info = self.get_trip_info()

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
        ).distinct().prefetch_related('cost_set','cost_set__splited_set', 'usertrip_set__user')

    def find_trip(self, trip_id):
        for trip in self.trip_details_objects:
            if trip.trip_id == trip_id:
                return trip
        return None

    def update_trip_details(self, trip_id, **kwargs):
        trip = self.find_trip(trip_id)
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
                        if trip in self.trip_details_objects:
                            self.trip_details_objects.remove(trip)
                    else:
                        setattr(trip, field, value)
                        trip.save()

    def get_trip_info(self):
        trip_details = []

        for trip in self.trip_details_objects:
            trip_info = {
                'trip_id': trip.trip_id, 'name': trip.name, 'start': trip.start, 'end': trip.end,
                'description': trip.description,
                'owner': {'user_id': trip.trip_owner.user_id, 'firstname': trip.trip_owner.firstname},
                'squad': [{'user_id': user_trip.user.user_id,'firstname': user_trip.user.firstname}
                    for user_trip in trip.usertrip_set.all()],
                'costs': {'own_cost' : 0, 'costs':[]}
            }

            for cost in trip.cost_set.all():
                splited_list = list(cost.splited_set.all())
                number_of_splited = len(splited_list)
                unit_cost = round(cost.value / number_of_splited if number_of_splited > 0 else 0, 2)
                user_in_splited = any(splited.user.user_id == self.user_id for splited in splited_list)
                unpaid_users = [splited.user for splited in splited_list if not splited.payment]

                cost_info = {
                    'cost_id': cost.cost_id, 'cost_name': cost.cost_name, 'value': cost.value,
                    'unit_cost': unit_cost,
                    'payer': {'user_id': cost.payer.user_id, 'firstname': cost.payer.firstname},
                    'splited': [{'user_id': splited.user.user_id,'payment': splited.payment}
                        for splited in splited_list],
                    'unpaid_users': [{'user_id': user.user_id, 'firstname':user.firstname, 'lastname':user.lastname,
                                      'get_cash_from_user': user.user_id != self.user_id,'unit_cost': unit_cost}
                        for user in unpaid_users]

                }


            trip_details.append(trip_info)

        return trip_details




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
        cost = self.find_cost(cost_id)
        splited = self.get_splited_info(cost_id)
        if cost and cost.payer_id == self.user_id:
            cost_to_update = {
                'cost_name': kwargs.get('cost_name'),
                'value': kwargs.get('value'),
                'payment':kwargs.get('payment'),
                'delete': kwargs.get('delete')
            }
            print(kwargs)

            for field, value in cost_to_update.items():
                if value != None:
                    if field == 'delete':
                        cost.delete()
                        if cost in self.trip_details_objects:
                            self.trip_details_objects.remove(cost)

                    elif field == 'payment':
                        split_user_id = kwargs.get('split_user_id')
                        split = next(split for split in splited if split.user_id == split_user_id)
                        split.payment = value
                        split.save()

                    else:
                        cost.field = value
                        cost.save()














