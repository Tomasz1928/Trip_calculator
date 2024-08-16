from trip_calculator.imp.trip_controller import get_user_CostController, get_user_TripController
from trip_calculator.imp.registration_controller import get_UserController
import ast, json

def add_trip(user_id, data):
    squad = ast.literal_eval(data['squad'])
    squad.append(user_id)
    instance = get_user_TripController(user_id)
    instance.new_trip(data['name'], data['start'], data['end'], data['description'], sorted(squad))

def manage_trip_action(user_id, data):
    action = data['action']
    instance = get_user_TripController(user_id)

    action_map = {
        'delete': lambda: instance.update_trip_details(data['trip_id'], delete=True),
        'description': lambda: instance.update_trip_details(data['trip_id'], description=data['description']),
        'title': lambda: instance.update_trip_details(data['trip_id'], name=data['name'])
    }
    action_map[action]()


def add_cost(user_id, trip_id, data):
    costs = ast.literal_eval(data['cost'])
    instance = get_user_CostController(user_id)
    for cost in costs:
        if cost['include'] == 'true':
            split_user_ids = [user_id] + [int(x) for x in cost['split']]
        else:
            split_user_ids = [int(x) for x in cost['split']]

        instance.add_cost(trip_id, cost['title'], cost['amount'], sorted(split_user_ids))


def manage_cost_action(user_id, data):
    action = data['action']
    instance = get_user_CostController(user_id)

    action_map = {
        'delete': lambda: instance.update_cost_details(data['cost_id'], delete=True),
        'update': lambda: instance.update_cost_details(data['cost_id'], value=data['value']),
        'status': lambda: instance.update_cost_details(data['cost_id'], payment=data['payment'], split_user_id=data['user_id']),
        'title': lambda: instance.update_cost_details(data['cost_id'], cost_name=data['name'])
    }

    action_map[action]()


def manage_account_action(data,*args, **kwargs):
    action = kwargs.get('action')
    instance = get_UserController()

    action_map = {
        'register': lambda: instance.register_user(data['email'], data['firstname'], data['lastname']),
        'recovery': lambda: instance.recovery(data['email']),
        'update': lambda: instance.update_user(args[0], **{key: value for key, value in data.items() if value and key != 'csrfmiddlewaretoken'}),
        'invite': lambda: invite_friend_helper_function(args[0], data)
    }

    def invite_friend_helper_function(user_id, new_friend):
        new_friend_data = json.loads(new_friend['friend'])
        for friend in new_friend_data:
            instance.invite_user(user_id, friend['email'], friend['firstname'], friend['lastname'])

    return action_map[action]()






