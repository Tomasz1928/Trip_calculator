from django.core.cache import cache
from django.db import transaction
from django.db.models import Q, Prefetch
from trip_calculator.models import Friend, UserTrip, Trip

class FriendController:
    def __init__(self, user_id):
        self.user_id = user_id
        self.friend_object = self.get_friend_object()

    def get_friend_object(self):
        return Friend.objects.filter(
            Q(user_id=self.user_id) |
            Q(friend_id=self.user_id)
        ).select_related('friend').distinct()

    def refresh_friend_object(self):
        self.friend_object = self.get_friend_object()

    def check_if_friend_exist(self, friend_id):
        return any(
            (friend.user_id == self.user_id and friend.friend_id == friend_id) or
            (friend.user_id == friend_id and friend.friend_id == self.user_id)
            for friend in self.friend_object
        )

    def add_friend(self, friend_id):
        if friend_id != self.user_id and not self.check_if_friend_exist(friend_id):
            with transaction.atomic():
                Friend.objects.create(user_id=self.user_id, friend_id=friend_id)
                Friend.objects.create(user_id=friend_id, friend_id=self.user_id)
            self.refresh_friend_object()

    def delete_friend(self, friend_id):
        if friend_id != self.user_id:
            Friend.objects.filter(
                Q(user_id=self.user_id, friend_id=friend_id) |
                Q(user_id=friend_id, friend_id=self.user_id)
            ).delete()
            self.refresh_friend_object()

    def get_friend_list(self):
        friends = Friend.objects.filter(user=self.user_id).select_related('friend')
        return [{'user_id': friend.friend.user_id, 'name': friend.friend.firstname, 'lastname': friend.friend.lastname}
                for friend in friends]

    def get_friend_list_for_trip(self):
        friends = Friend.objects.filter(user_id=self.user_id).select_related('friend').prefetch_related(
            Prefetch('friend__usertrip_set', queryset=UserTrip.objects.filter(
                trip_id__in=UserTrip.objects.filter(user_id=self.user_id).values_list('trip_id', flat=True)
            ).select_related('trip'), to_attr='common_trips')
        )

        trip_ids = {trip.trip_id for friend in friends for trip in friend.friend.common_trips}
        trips = Trip.objects.filter(trip_id__in=trip_ids)
        trip_name_map = {trip.trip_id: trip.name for trip in trips}

        return [
            {'name': friend.friend.firstname, 'lastname': friend.friend.lastname,
             'added': friend.created_at.strftime("%d.%m.%Y"), 'user_id': friend.friend.user_id,
             'trips': [{'name': trip_name_map.get(trip.trip_id)} for trip in friend.friend.common_trips]}
            for friend in friends
        ]


def get_user_FriendController(user_id):
    cache_key = f"FriendController{user_id}"
    service = cache.get(cache_key)

    if not service:
        service = FriendController(user_id)
        cache.set(cache_key, service, timeout=60 * 30)

    return service
