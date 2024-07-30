from django.db import transaction
from trip_calculator.models import Cost, Splited, User
import ast


def get_trip_controller():
    from trip_calculator.imp.trip_controller import TripController
    return TripController()


class CostController:
    def add_cost(self, payer_id, trip_id, name, value, split_user_ids):
        with transaction.atomic():
            new_cost = Cost(trip_id=trip_id, payer_id=payer_id, cost_name=name, value=value)
            new_cost.save()
            splits = [Splited(cost=new_cost, user_id=user_id, payment=(payer_id == user_id)) for user_id in split_user_ids]
            Splited.objects.bulk_create(splits)

    def remove_cost(self, cost_id):
        cost = Cost.objects.get(cost_id=cost_id)
        cost.delete()

    def edit_value(self, cost_id, value):
        cost = Cost.objects.get(cost_id=cost_id)
        cost.value = value
        cost.save()

    def edit_name(self, cost_id, title):
        cost = Cost.objects.get(cost_id=cost_id)
        cost.cost_name = title
        cost.save()

    def _get_user_details(self, user_ids):
        users = User.objects.filter(user_id__in=user_ids)
        return {
            user.user_id: {'firstname': user.firstname, 'lastname': user.lastname, 'user_id': user.user_id}
            for user in users
        }

    def check_if_user_isPayer(self, user_id, cost_id):
        cost = Cost.objects.get(cost_id=cost_id)
        return cost.payer.user_id == user_id

    def get_all_cost_from_trip_id(self, trip_id):
        costs = Cost.objects.filter(trip_id=trip_id).prefetch_related('splited_set', 'payer')
        cost_details = []
        for cost in costs:
            split_details = cost.splited_set.values('user_id', 'payment')
            split_users = [
                {'user_id': detail['user_id'], 'payment': detail['payment'],
                 'firstname': User.objects.get_user_by_id(detail['user_id']).firstname,
                 'lastname': User.objects.get_user_by_id(detail['user_id']).lastname}
                for detail in split_details
            ]
            payer = self._get_user_details([cost.payer.user_id]).get(cost.payer.user_id)
            cost_details.append({'split': split_users, 'payer': payer, 'cost_name': cost.cost_name, 'value': cost.value,
                                 'cost_id': cost.cost_id})
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
    cost_controller = CostController()
    for cost in costs:
        split_user_ids = [user_id] + [int(x) for x in cost['split']]
        cost_controller.add_cost(user_id, trip_id, cost['title'], cost['amount'], sorted(split_user_ids))


def delete_cost(data):
    CostController().remove_cost(data['cost_id'])


def update_cost_value(data):
    CostController().edit_value(data['cost_id'], data['value'])


def update_cost_title(data):
    CostController().edit_name(data['cost_id'], data['name'])


def update_cost_status(data):
    status_update = Splited.objects.get(cost_id=data['cost_id'], user_id=data['user_id'])
    status_update.payment = data['payment']
    status_update.save()


def manage_cost_action(user_id, data):
    action = data['action']

    if action not in ['delete', 'update', 'status', 'title']:
        raise ValueError("Invalid action specified")

    if not CostController().check_if_user_isPayer(user_id, data['cost_id']):
        raise PermissionError("User is not authorized to perform this action")

    action_map = {
        'delete': lambda: delete_cost(data),
        'update': lambda: update_cost_value(data),
        'status': lambda: update_cost_status(data),
        'title': lambda: update_cost_title(data)
    }

    action_map[action]()


def get_all_cost_details(user_id):
    trip_controller = get_trip_controller()
    trip_ids = trip_controller.get_all_trip_id_for_user(user_id)
    trip_data = []
    all_cost = {'any': bool(trip_ids), 'for_trip': []}

    cost_controller = CostController()

    for trip_id in trip_ids:
        trip_details = trip_controller.get_trip_detail_by_trip_id(trip_id, user_id)
        costs_data = cost_controller.get_all_cost_from_trip_id(trip_id)

        costs = []
        for cost_data in costs_data:
            if any(user['user_id'] == user_id for user in cost_data['split']):
                data = calculate_to_return(cost_data, user_id)
                cost = {
                    'cost_id': cost_data['cost_id'], 'name': cost_data['cost_name'],
                    'who_pay': {'name': cost_data['payer']['firstname'], 'lastname': cost_data['payer']['lastname'],
                                'was_you': data["payer_was_you"]}, 'cost': str(cost_data['value']),
                    'split_by': cost_data['split'], 'unit_cost': str(data['unit_cost']),
                    'return': str(data['to_return']), 'balance': data['balance']
                }
                costs.append(cost)

        trip_data.append({
            'id': str(trip_id), 'name': trip_details['name'],
            'self_cost': str(round(cost_controller.get_all_trip_cost_for_user_id(trip_id, user_id), 2)), 'costs': costs,
            'balance': round(sum(float(cost['balance']) for cost in costs), 2)
        })

    all_cost['for_trip'] = trip_data
    return all_cost


def calculate_to_return(cost_data, user_id):
    payer_was_you = CostController().check_if_user_isPayer(user_id, cost_data['cost_id'])
    unit_cost = round(cost_data['value'] / len(cost_data['split']), 2)

    if payer_was_you:
        count_user_who_dont_pay = sum(1 for user in cost_data['split'] if not user['payment'])
        return {'payer_was_you': payer_was_you, 'unit_cost': unit_cost,
                'to_return': unit_cost * count_user_who_dont_pay,
                'balance': unit_cost * count_user_who_dont_pay}
    else:
        user_data = next(user for user in cost_data['split'] if user['user_id'] == user_id)
        return {'payer_was_you': payer_was_you, 'unit_cost': unit_cost,
                'to_return': 0 if user_data['payment'] else unit_cost,
                'balance': 0 if user_data['payment'] else (-unit_cost)}





