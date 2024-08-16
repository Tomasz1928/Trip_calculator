from trip_calculator.models import User
from django.contrib.auth.hashers import make_password
from trip_calculator.imp.email_controller import EmailSender
import json, secrets, string
from trip_calculator.imp.friend_controller import get_user_FriendController
from django.core.cache import cache


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

class UserController:

    def _create_user_in_DB_(self, email, firstname, lastname, password_hashed):
        user = User(email=email, firstname=firstname, lastname=lastname, password=password_hashed)
        user.save()

    def update_user(self, user_id, **kwargs):
        update_user = User.objects.get_user_by_id(user_id)

        fields_to_update = {
            'firstname': kwargs.get('firstname'),
            'lastname': kwargs.get('lastname'),
            'email': kwargs.get('email'),
            'password': kwargs.get('password')
        }

        for field, value in fields_to_update.items():
            if value:
                if field == 'password':
                    update_user.password = make_password(value)
                    send = EmailSender(User.objects.get_user_by_id(user_id).email, value)
                    send.send_email('update_password')
                else:
                    setattr(update_user, field, value)
        update_user.save()

    def check_if_email_exists(self, email):
        return User.objects.filter(email=email).exists()

    def register_user(self, email, firstname, lastname, *args):
        password = generate_random_password()
        password_hashed = make_password(password)
        self._create_user_in_DB_(email, firstname, lastname, password_hashed)
        send = EmailSender(email, password)
        send.send_email(args[0] if args else 'registration')
        return {"registration_pass": True}

    def invite_user(self, user_id, email, firstname, lastname):
        if self.check_if_email_exists(email):
            friend_id = User.objects.get_by_natural_key(email).user_id
            get_user_FriendController(user_id).add_friend(friend_id)
        else:
            self.register_user(email,firstname, lastname, 'invitation')
            get_user_FriendController(user_id).add_friend(User.objects.get_by_natural_key(email).user_id)

    def recovery(self, email):
        if self.check_if_email_exists(email):
            new_password = generate_random_password()
            user = User.objects.get_by_natural_key(email)
            user.password = make_password(new_password)
            user.save()

            recovery_message = EmailSender(email, new_password)
            recovery_message.send_email('recovery')
            return {"recovery_pass": True}
        else:
            return {"recovery_pass": False}

def get_UserController():
    cache_key = f"UserController"
    service = cache.get(cache_key)

    if not service:
        service = UserController()
        cache.set(cache_key, service, timeout=60 * 30)
    return service

def get_user_infor(user_id):
    data = User.objects.get_user_by_id(user_id)
    return {'name': data.firstname, 'lastname': data.lastname, 'email': data.email, 'added': data.created_at.strftime("%d.%m.%Y"), 'user_id': user_id}
