from trip_calculator.models import Friend, UserTrip, Trip
from django.db.models import Q
from django.db import transaction

class FriendController:
    def __init__(self, user_id):
        self.user_id = user_id

    def _set_friend_id(self, friend_id):
        self.friend_id = friend_id

    def _check_friend_not_exists(self):
        return not Friend.objects.filter(
            Q(user_id=self.user_id, friend_id=self.friend_id) |
            Q(user_id=self.friend_id, friend_id=self.user_id)
        ).exists()

    def add_friend(self, friend_id):
        self._set_friend_id(friend_id)
        if self._check_friend_not_exists() and friend_id != self.user_id:
            with transaction.atomic():
                Friend.objects.create(user_id=self.user_id, friend_id=self.friend_id)
                Friend.objects.create(user_id=self.friend_id, friend_id=self.user_id)

    def delete_friend(self, friend_id):
        self._set_friend_id(friend_id)
        with transaction.atomic():
            Friend.objects.filter(
                Q(user_id=self.user_id, friend_id=self.friend_id) |
                Q(user_id=self.friend_id, friend_id=self.user_id)
            ).delete()

    def get_friend_list(self):
        friends = Friend.objects.filter(user_id=self.user_id).select_related('friend')
        friend_details_list = []

        friend_ids = [friend.friend_id for friend in friends]
        common_trip_ids = UserTrip.objects.filter(
            user_id=self.user_id,
            trip_id__in=UserTrip.objects.filter(user_id__in=friend_ids).values_list('trip_id', flat=True)
        ).values_list('trip_id', flat=True)

        trip_name_map = {trip.trip_id: trip.name for trip in Trip.objects.filter(trip_id__in=common_trip_ids)}

        for friend in friends:
            common_trips = UserTrip.objects.filter(user_id=friend.friend_id, trip_id__in=common_trip_ids)
            common_trip_names = [trip_name_map.get(trip.trip_id) for trip in common_trips]

            friend_detail = {
                'name': friend.friend.firstname,
                'lastname': friend.friend.lastname,
                'added': friend.created_at.strftime("%d.%m.%Y"),
                'user_id': friend.friend.user_id,
                'trips': [{'name': trip_name} for trip_name in common_trip_names]
            }
            friend_details_list.append(friend_detail)

        return friend_details_list