from trip_calculator.models import Trip, Cost, Splited, User, UserTrip
from django.shortcuts import get_object_or_404
from django.db import transaction
import ast, json


class TripController:

    def __init__(self):
        pass

    def add_trip(self, name, start, end, description, squad):
        with transaction.atomic():
            new_trip = Trip(name=name, start=start, end=end, description=description)
            new_trip.save()
            user_trips = [UserTrip(trip=new_trip, user_id=user_id) for user_id in squad]
            UserTrip.objects.bulk_create(user_trips)

    def get_all_trip_id_for_user(self, user_id):
        return UserTrip.objects.filter(user_id=user_id).values_list('trip_id', flat=True)

    def get_trip_squad(self, trip_id):
        user_trips = UserTrip.objects.filter(trip_id=trip_id).select_related('user')
        return [
            {'firstname': user.firstname, 'lastname': user.lastname, 'user_id': user.user_id}
            for user_trip in user_trips
            for user in [user_trip.user]
        ]

    def get_trip_detail_by_trip_id(self, trip_id, user_id):
        trip_data = get_object_or_404(Trip, pk=trip_id)
        squad = self.get_trip_squad(trip_id)
        cost = CostController().get_all_trip_cost_for_user_id(trip_id, user_id)
        return {'squad': squad, 'name': trip_data.name, 'description': trip_data.description, 'cost': cost}


class CostController:
    def add_cost(self, payer, trip_id, name, value, split):
        with transaction.atomic():
            new_cost = Cost(trip_id=trip_id, payer_id=payer, cost_name=name, value=value)
            new_cost.save()
            splits = [Splited(cost=new_cost, user_id=user_id) for user_id in split]
            Splited.objects.bulk_create(splits)

    def _get_user_details(self, user_ids):
        users = User.objects.filter(user_id__in=user_ids)
        return {
            user.user_id: {'firstname': user.firstname, 'lastname': user.lastname, 'user_id': user.user_id}
            for user in users
        }

    def get_all_cost_from_trip_id(self, trip_id):
        costs = Cost.objects.filter(trip_id=trip_id).prefetch_related('splited_set', 'payer')
        cost_details = []
        for cost in costs:
            split_users = self._get_user_details(cost.splited_set.values_list('user_id', flat=True))
            payer = self._get_user_details([cost.payer.user_id]).get(cost.payer.user_id)
            cost_details.append({
                'split': list(split_users.values()), 'payer': payer, 'cost_name': cost.cost_name, 'value': cost.value
            })
        return cost_details

    def get_all_trip_cost_for_user_id(self, trip_id, user_id):
        costs = Cost.objects.filter(trip_id=trip_id).prefetch_related('splited_set')
        total_cost = 0
        for cost in costs:
            splits = cost.splited_set.count()
            if splits > 0 and Splited.objects.filter(cost=cost, user=user_id).exists():
                total_cost += cost.value / splits
        return total_cost


def add_trip(user_id, data):
    squad = ast.literal_eval(data['squad'])
    squad.append(user_id)
    TripController().add_trip(data['name'], data['start'], data['end'], data['description'], sorted(squad))


def get_all_trips_with_details(user_id):
    trip_controller = TripController()
    trip_ids = trip_controller.get_all_trip_id_for_user(user_id)
    return [trip_controller.get_trip_detail_by_trip_id(trip_id, user_id) for trip_id in trip_ids]


def add_cost(user_id, trip_id, data):
    costs = ast.literal_eval(data['cost'])
    for cost in costs:
        split = [user_id] + [int(x) for x in cost['split']]
        CostController().add_cost(user_id, trip_id, cost['title'], cost['amount'], sorted(split))


def get_all_cost_details(user_id):
    all_cost = {'any': False, 'for_trip': []}
    trip_ids = TripController().get_all_trip_id_for_user(user_id)
    trip_data = []
    for trip_id in trip_ids:
        trip_details = TripController().get_trip_detail_by_trip_id(trip_id, user_id)
        cost_for_trip = {'id': str(trip_id),
                         'name': trip_details['name'],
                         'self_cost': str(CostController().get_all_trip_cost_for_user_id(trip_id, user_id)),
                         'costs': []}

        costs_data = CostController().get_all_cost_from_trip_id(trip_id)
        if len(costs_data) > 0:
            all_cost['any'] = True

        for cost_data in costs_data:
            if any(user['user_id'] == user_id for user in cost_data['split']):

                payer_was_you = True if cost_data['payer']['user_id'] == user_id else False

                unit_cost = cost_data['value'] / len(cost_data['split'])
                to_return = unit_cost * (len(cost_data['split']) - 1) if payer_was_you else unit_cost

                cost = {'name': cost_data['cost_name'],
                        'who_pay': {'name': cost_data['payer']['firstname'],
                                    'was_you': payer_was_you},
                         'cost': str(cost_data['value']),
                         'split_by': cost_data['split'],
                         'unit_cost': str(unit_cost),
                         'return': str(to_return)}
                cost_for_trip['costs'].append(cost)

        cost_for_trip['balance'] = 0
        for cost in cost_for_trip['costs']:
            cost_for_trip['balance'] += float(cost['cost'])

        trip_data.append(cost_for_trip)


    all_cost['for_trip'] = trip_data
    return all_cost