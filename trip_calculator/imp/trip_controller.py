from trip_calculator.models import Trip, UserTrip
from django.shortcuts import get_object_or_404
from django.db import transaction
import ast

def get_cost_controller():
    from trip_calculator.imp.cost_controller import CostController
    return CostController()

class TripController:

    def __init__(self):
        pass

    def add_trip(self, name, start, end, description, squad, owner):
        with transaction.atomic():
            new_trip = Trip(name=name, start=start, end=end, description=description, trip_owner_id=owner)
            new_trip.save()
            user_trips = [UserTrip(trip=new_trip, user_id=user_id) for user_id in squad]
            UserTrip.objects.bulk_create(user_trips)

    def delete_trip(self, trip_id):
        with transaction.atomic():
            trip = Trip.objects.get(pk=trip_id)
            trip.delete()

    def update_trip(self, trip_id, **kwargs):
        trip = Trip.objects.get(pk=trip_id)

        fields_to_update = {
            'name': kwargs.get('name'),
            'description': kwargs.get('description'),
            'delete': kwargs.get('delete')
        }


        for field, value in fields_to_update.items():
            if value:
                if field == 'delete':
                    self.delete_trip(trip_id)
                else:
                    setattr(trip, field, value)
        trip.save()


    def check_if_user_isTripOwner(self, user_id, trip_id):
        owner = Trip.objects.get(pk=trip_id)
        return owner.trip_owner.user_id == user_id

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
        cost_controller = get_cost_controller()
        trip_data = get_object_or_404(Trip, pk=trip_id)
        squad = self.get_trip_squad(trip_id)
        cost = round(cost_controller.get_all_trip_cost_for_user_id(trip_id, user_id), 2)
        return {'squad': squad, 'name': trip_data.name, 'description': trip_data.description, 'cost': cost,
                'owner': self.check_if_user_isTripOwner(user_id, trip_id), 'trip_id': trip_id}


def add_trip(user_id, data):
    squad = ast.literal_eval(data['squad'])
    squad.append(user_id)
    TripController().add_trip(data['name'], data['start'], data['end'], data['description'], sorted(squad), int(user_id))


def get_all_trips_with_details(user_id):
    trip_controller = TripController()
    trip_ids = trip_controller.get_all_trip_id_for_user(user_id)
    return [trip_controller.get_trip_detail_by_trip_id(trip_id, user_id) for trip_id in trip_ids]


def remove_trip(user_id, data):
    if TripController().check_if_user_isTripOwner(user_id, data['trip_id']):
        TripController().delete_trip(data['trip_id'])


def update_trip(user_id, data):
    if TripController().check_if_user_isTripOwner(user_id, data['trip_id']):
        kwargs = {key: value for key, value in data.items() if value}
        trip_id = int(kwargs['trip_id'])
        kwargs.pop('csrfmiddlewaretoken', None)
        kwargs.pop('trip_id', None)
        TripController().update_trip(trip_id, **kwargs)

