from trip_calculator.models import Friend, User
class AddFriend:
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

        friend_list = Friend.objects.filter(user_id=self.user_id)
        friend_detail_list = []
        for friend in friend_list:
            friend_detail = User.objects.get_user_by_ID(friend.friend_id)
            friend_detail_list.append({'name': friend_detail.firstname, 'lastname': friend_detail.lastname, 'added': friend.created_at})
        return friend_detail_list
