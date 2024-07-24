from trip_calculator.models import Friend, User, UserTrip, Trip
from datetime import datetime, timezone


class FriendController:
    def __init__(self, user_id):
        self.user_id = user_id
        self.friend_id = ''

    def set_friend_id(self, friend_id):
        self.friend_id = friend_id

    def _check_friend_not_exists_(self):
        return not Friend.objects.filter(user_id=self.user_id, friend_id=self.friend_id).exists()

    def add_friend(self, friend_id):
        self.set_friend_id(friend_id)
        if self._check_friend_not_exists_():
            new_friend_for_user = Friend(user_id=self.user_id, friend_id=self.friend_id)
            new_friend_for_user.save()
            new_friend_for_friend = Friend(user_id=self.friend_id, friend_id=self.user_id)
            new_friend_for_friend.save()

    def delete_friend(self, friend_id):
        self.set_friend_id(friend_id)
        delete_friend_for_user = Friend.objects.get(user_id=self.user_id, friend_id=self.friend_id)
        delete_friend_for_user.delete()
        delete_friend_for_friend = Friend.objects.get(user_id=self.friend_id, friend_id=self.user_id)
        delete_friend_for_friend.delete()

    def get_Friend_list(self):
        sql_query = Friend.objects.filter(user_id=self.user_id)
        friend_detail_list = []

        for obj in sql_query:
            friend_add_date = obj.created_at
            sql_query2 = UserTrip.objects.filter(user_id=obj.user_id)
            common_trip_name_list = []

            for obj2 in sql_query2:
                common_trip_id = UserTrip.objects.get(user_id=self.user_id, trip_id = obj2.trip_id)
                comon_trip_name = Trip.objects.get(trip_id= common_trip_id.trip_id)
                common_trip_name_list.append({'name': comon_trip_name.name})

            friend_detail = User.objects.get_user_by_ID(obj.friend_id)
            data = {'name': friend_detail.firstname,
                    'lastname': friend_detail.lastname,
                    'added': friend_add_date.strftime("%d.%m.%Y"),
                    'user_id': friend_detail.user_id,
                    'trips': common_trip_name_list
                    }
            friend_detail_list.append(data)
        return friend_detail_list
