from trip_calculator.models import Friend, UserTrip, Trip
from django.db.models import Q, Prefetch
from django.db import transaction

class FriendController:
    def __init__(self, user_id):
        self.user_id = user_id

    def update_info(self):
        return Friend.objects.filter(
            Q(user_id=self.user_id) |
            Q(friend_id=self.user_id)
        ).select_related('friend').distinct()

    def check_if_friend_exist(self, friend_id):
        return Friend.objects.filter(
            Q(user_id=self.user_id, friend_id=friend_id) |
            Q(user_id=friend_id, friend_id=self.user_id)
        ).exists()

    def add_friend(self, friend_id):
        if friend_id != self.user_id and not self.check_if_friend_exist(friend_id):
            with transaction.atomic():
                Friend.objects.create(user_id=self.user_id, friend_id=friend_id)
                Friend.objects.create(user_id=friend_id, friend_id=self.user_id)

    def delete_friend(self, friend_id):
        if friend_id != self.user_id:
            Friend.objects.filter(
                Q(user_id=self.user_id, friend_id=friend_id) |
                Q(user_id=friend_id, friend_id=self.user_id)
            ).delete()

    def get_friend_list(self):
        friends = Friend.objects.filter(user_id=self.user_id).select_related('friend').prefetch_related(
            Prefetch('friend__usertrip_set', queryset=UserTrip.objects.filter(
                trip_id__in=UserTrip.objects.filter(user_id=self.user_id).values_list('trip_id', flat=True)),
                     to_attr='common_trips'))

        trip_name_map = {
            trip.trip_id: trip.name for trip in Trip.objects.filter(
                trip_id__in=UserTrip
                .objects.filter(user_id=self.user_id,
                                trip_id__in=[trip.trip_id for friend in friends for trip in friend.friend.common_trips])
                .values_list('trip_id', flat=True).distinct())
        }

        return [
            {'name': friend.friend.firstname, 'lastname': friend.friend.lastname,
             'added': friend.created_at.strftime("%d.%m.%Y"), 'user_id': friend.friend.user_id,
             'trips': [{'name': trip_name_map.get(trip.trip_id)} for trip in friend.friend.common_trips]}
            for friend in friends
        ]
