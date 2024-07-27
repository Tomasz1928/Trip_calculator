from trip_calculator.models import Friend, UserTrip, Trip

class FriendController:
    def __init__(self, user_id):
        self.user_id = user_id

    def _set_friend_id(self, friend_id):
        self.friend_id = friend_id

    def _check_friend_not_exists(self):
        return not Friend.objects.filter(user_id=self.user_id, friend_id=self.friend_id).exists()

    def add_friend(self, friend_id):
        self._set_friend_id(friend_id)
        if self._check_friend_not_exists():
            Friend.objects.create(user_id=self.user_id, friend_id=self.friend_id)
            Friend.objects.create(user_id=self.friend_id, friend_id=self.user_id)

    def delete_friend(self, friend_id):
        self._set_friend_id(friend_id)
        Friend.objects.filter(user_id=self.user_id, friend_id=self.friend_id).delete()
        Friend.objects.filter(user_id=self.friend_id, friend_id=self.user_id).delete()

    def get_friend_list(self):
        friends = Friend.objects.filter(user_id=self.user_id).select_related('friend')
        friend_details_list = []

        for friend in friends:
            friend_add_date = friend.created_at
            common_trips = UserTrip.objects.filter(user_id=self.user_id, trip_id__in=UserTrip.objects.filter(user_id=friend.friend_id).values_list('trip_id', flat=True))
            common_trip_names = [Trip.objects.get(trip_id=common_trip.trip_id).name for common_trip in common_trips]

            friend_detail = {
                'name': friend.friend.firstname,
                'lastname': friend.friend.lastname,
                'added': friend_add_date.strftime("%d.%m.%Y"),
                'user_id': friend.friend.user_id,
                'trips': [{'name': trip_name} for trip_name in common_trip_names]
            }
            friend_details_list.append(friend_detail)

        return friend_details_list