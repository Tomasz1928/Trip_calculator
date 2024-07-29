from trip_calculator.models import Cost, Splited, User
from django.db import transaction
import ast


def get_trip_controller():
    from trip_calculator.imp.trip_controller import TripController
    return TripController()

class CostController:
    def add_cost(self, payer, trip_id, name, value, split):
        with transaction.atomic():
            new_cost = Cost(trip_id=trip_id, payer_id=payer, cost_name=name, value=value)
            new_cost.save()

            splits = []
            for user_id in split:
                is_payment = (payer == user_id)
                splits.append(Splited(cost=new_cost, user_id=user_id, payment=is_payment))

            Splited.objects.bulk_create(splits)

    def _get_user_details(self, user_ids):
        users = User.objects.filter(user_id__in=user_ids)
        return {
            user.user_id: {'firstname': user.firstname, 'lastname': user.lastname, 'user_id': user.user_id}
            for user in users}


    def get_all_cost_from_trip_id(self, trip_id):
        costs = Cost.objects.filter(trip_id=trip_id).prefetch_related('splited_set', 'payer')
        cost_details = []
        for cost in costs:
            split_details = cost.splited_set.values('user_id', 'payment')
            split_users = [{'user_id': detail['user_id'], 'payment': detail['payment'],
                            'firstname': User.objects.get_user_by_id(detail['user_id']).firstname} for detail in split_details]
            payer_user_id = cost.payer.user_id
            payer = self._get_user_details([payer_user_id]).get(payer_user_id)
            cost_details.append({'split': split_users, 'payer': payer, 'cost_name': cost.cost_name,
                                 'value': cost.value, 'cost_id': cost.cost_id})
        return cost_details

    def get_all_trip_cost_for_user_id(self, trip_id, user_id):
        costs = Cost.objects.filter(trip_id=trip_id).prefetch_related('splited_set')
        total_cost = 0
        for cost in costs:
            splits = cost.splited_set.count()
            if splits > 0 and Splited.objects.filter(cost=cost, user=user_id).exists():
                total_cost += cost.value / splits
        return total_cost


def add_cost(user_id, trip_id, data):
    costs = ast.literal_eval(data['cost'])
    for cost in costs:
        split = [user_id] + [int(x) for x in cost['split']]
        CostController().add_cost(user_id, trip_id, cost['title'], cost['amount'], sorted(split))


def costStatusUpdate(data):
    status_update = Splited.objects.get(cost_id=data['cost_id'], user_id=data['user_id'])
    status_update.payment = data['payment']
    status_update.save()


def get_all_cost_details(user_id):
    trip_controller = get_trip_controller()
    all_cost = {'any': False, 'for_trip': []}
    trip_ids = trip_controller.get_all_trip_id_for_user(user_id)
    trip_data = []

    if len(trip_ids) > 0:
        all_cost['any'] = True

    for trip_id in trip_ids:
        trip_details = trip_controller.get_trip_detail_by_trip_id(trip_id, user_id)
        cost_for_trip = {'id': str(trip_id),
                         'name': trip_details['name'],
                         'self_cost': str(CostController().get_all_trip_cost_for_user_id(trip_id, user_id)),
                         'costs': []}

        costs_data = CostController().get_all_cost_from_trip_id(trip_id)

        for cost_data in costs_data:
            if any(user['user_id'] == user_id for user in cost_data['split']):
                data = ToReturn(cost_data, user_id)
                cost = {'cost_id': cost_data['cost_id'],
                        'name': cost_data['cost_name'],
                        'who_pay': {'name': cost_data['payer']['firstname'],
                                    'was_you': data["payer_was_you"]},
                         'cost': str(cost_data['value']),
                         'split_by': cost_data['split'],
                         'unit_cost': str(data['unit_cost']),
                         'return': str(data['to_return'])}
                cost_for_trip['costs'].append(cost)

        cost_for_trip['balance'] = 0
        for cost in cost_for_trip['costs']:
            cost_for_trip['balance'] += float(cost['cost'])

        trip_data.append(cost_for_trip)

    all_cost['for_trip'] = trip_data
    return all_cost


def ToReturn(cost_data, user_id):
    payer_was_you = True if cost_data['payer']['user_id'] == user_id else False
    unit_cost = round(cost_data['value'] / len(cost_data['split']), 2)

    data = {'payer_was_you': payer_was_you, 'unit_cost': unit_cost}

    if payer_was_you:
        count_user_who_dont_pay = sum(1 for user in cost_data['split'] if user['payment'] == False)
        data['to_return'] = unit_cost * count_user_who_dont_pay

    else:
        user_data = [user for user in cost_data['split'] if user['user_id'] == user_id][0]
        if user_data['payment']:
            data['to_return'] = 0
        else:
            data['to_return'] = unit_cost
    return data
