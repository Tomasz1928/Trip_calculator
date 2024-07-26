from trip_calculator.models import Trip, Cost, Splited, User, UserTrip
import ast, json


class TripController:

    def __init__(self):
        self.name = ''
        self.start = ''
        self.end = ''
        self.description = ''

    def add_trip(self, name, start, end, description, squad):
        new_trip = Trip(name=name, start=start, end=end, description=description)
        new_trip.save()
        trip_id = new_trip.trip_id
        for user_id in squad:
            squad = UserTrip(trip_id=trip_id, user_id=user_id)
            squad.save()


    def get_all_trip_id_for_user(self, user_id):
        sql_query = UserTrip.objects.filter(user_id=user_id)
        trip_id_list = []
        for obj in sql_query:
            trip_id_list.append(obj.trip_id)
        return trip_id_list

    def get_trip_squad(self, trip_id):
        sql_query = UserTrip.objects.filter(trip_id=trip_id)
        trip_squad_list = []
        for obj in sql_query:
            user = User.objects.get_user_by_ID(obj.user_id)
            data = {'firstname': user.firstname, 'lastname':  user.lastname, 'user_id': user.user_id}
            trip_squad_list.append(data)
        return trip_squad_list

    def get_trip_detail_by_trip_id(self, trip_id, user_id):
        trip_data = Trip.objects.get(trip_id=trip_id)
        squad = self.get_trip_squad(trip_id)
        cost = CostController().get_all_trip_cost_for_user_id(trip_id, user_id)
        data = {'squad': squad, 'name': trip_data.name, 'description': trip_data.description, 'cost': cost }
        return data



class CostController:
    def add_cost(self, payer, trip_id, name, value, split):
        new_cost = Cost(trip_id_id=trip_id, payer_id_id=payer, cost_name=name, value=value)
        new_cost.save()
        cost_id = new_cost.cost_id
        for user_id in split:
            spilt = Splited(cost_id_id=cost_id, user_id_id=user_id)
            spilt.save()

    def _get_friend_detail_from_split_id_(self, cost_id):
        sql_query = Splited.objects.filter(cost_id_id=cost_id)
        split_list = []
        for obj in sql_query:
            user = User.objects.get_user_by_ID(obj.user_id_id)
            data = {'firstname': user.firstname, 'lastname': user.lastname, 'user_id': user.user_id}
            split_list.append(data)
        return split_list

    def _get_payer_details_from_payer_id_(self, payer_id):
        user = User.objects.get_user_by_ID(payer_id)
        data = {'firstname': user.firstname, 'lastname': user.lastname, 'user_id': user.user_id}
        return data

    def get_all_cost_from_trip_id(self, trip_id):
        sql_query = Cost.objects.filter(trip_id_id=trip_id)
        trip_cost = []
        for obj in sql_query:
            split_list = self._get_friend_detail_from_split_id_(obj.cost_id)
            payer = self._get_payer_details_from_payer_id_(obj.payer_id_id)
            data = {'split': split_list, 'payer': payer, 'cost_name': obj.cost_name, 'value': obj.value}
            trip_cost.append(data)
        return trip_cost

    def get_all_trip_cost_for_user_id(self, trip_id, user_id):
        sql_query = Cost.objects.filter(trip_id_id=trip_id)
        trip_cost = 0
        for obj in sql_query:
            if Splited.objects.filter(cost_id_id=obj.cost_id, user_id_id=user_id).exists():
                trip_cost = trip_cost + (obj.value / Splited.objects.filter(cost_id_id=obj.cost_id).count())

        return trip_cost


def add_trip(user_id, data):
    squad = ast.literal_eval(data['squad'])
    squad.append(user_id)
    TripController().add_trip(data['name'], data['start'], data['end'], data['description'], sorted(squad))


def add_cost(user_id, trip_id, data):
    for cost in ast.literal_eval(data['cost']):
        split = cost['split']
        split.append(user_id)
        split = [int(x) for x in split]
        CostController().add_cost(user_id, trip_id, cost['title'], cost['amount'], sorted(split))


def get_all_trips_with_details(user_id):
    trip = TripController()
    trip_list = trip.get_all_trip_id_for_user(user_id)
    details = []
    for trip_id in trip_list:
        details.append(trip.get_trip_detail_by_trip_id(trip_id, user_id))
    return details
