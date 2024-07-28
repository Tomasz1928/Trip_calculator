from trip_calculator.models import User
from django.contrib.auth.hashers import make_password
from trip_calculator.imp.email_controller import EmailSender
import json, secrets, string
from trip_calculator.imp.friend_controller import FriendController


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

class UserController:
    def __init__(self):
        pass

    def _create_user_in_DB_(self, email, firstname, lastname, password_hashed):
        if not email:
            raise ValueError("The Email field must be set")
        user = User(
            email=email,
            firstname=firstname,
            lastname=lastname,
            password=password_hashed
        )
        user.save()
        return user

    def update_user(self, user_id, **kwargs):
        update_user = User.objects.get_user_by_id(user_id)

        if 'firstname' in kwargs and kwargs['firstname']:
            update_user.firstname = kwargs['firstname']

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
                else:
                    setattr(update_user, field, value)
        update_user.save()

    def check_if_email_exists(self, email):
        return User.objects.filter(email=email).exists()

    def register_user(self, email, firstname, lastname):
        if self.check_if_email_exists(email):
            return {"registration_pass": False}
        else:
            password = generate_random_password()
            password_hashed = make_password(password)
            self._create_user_in_DB_(email, firstname, lastname, password_hashed)
            send = EmailSender()
            send.set_email(email)
            send.set_password(password)
            send.generate_registration_message()
            send.send_email()
            return {"registration_pass": True}

    def invite_user(self, user_id, email, firstname, lastname):
        if self.check_if_email_exists(email):
            friend_id = User.objects.get_by_natural_key(email).user_id
            new_friend = FriendController(user_id)
            new_friend.add_friend(friend_id)
            return {"registration_pass": False}
        else:
            password = generate_random_password()
            password_hashed = make_password(password)
            self._create_user_in_DB_(email, firstname, lastname, password_hashed)

            new_friend = FriendController(user_id)
            new_friend.add_friend(User.objects.get_by_natural_key(email).user_id)

            send = EmailSender()
            send.set_email(email)
            send.set_password(password)
            send.generate_invitation_message()
            send.send_email()
            return {"registration_pass": True}

    def recovery(self, email):
        if self.check_if_email_exists(email):
            user = User.objects.get_by_natural_key(email).user_id
            new_password = generate_random_password()
            self.update_user(user, password=new_password)
            recovery_message = EmailSender()
            recovery_message.set_email(email)
            recovery_message.set_password(new_password)
            recovery_message.generate_recovery_message()
            recovery_message.send_email()
            return {"recovery_pass": True}
        else:
            return {"recovery_pass": False}


def registration(data):
    return UserController().register_user(data['email'], data['firstname'], data['lastname'])


def recovery(data):
    return UserController().recovery(data['email'])


def get_user_infor(user_id):
    data = User.objects.get_user_by_id(user_id)
    return {'name': data.firstname, 'lastname': data.lastname, 'email': data.email, 'added': data.created_at.strftime("%d.%m.%Y"), 'user_id': user_id}


def update_account(user_id, data):
    kwargs = {key: value for key, value in data.items() if value}
    kwargs.pop('csrfmiddlewaretoken', None)
    print(kwargs)


def invite_user(user_id, data):
    friends_data = json.loads(data['friend'])
    for friend in friends_data:
        UserController().invite_user(user_id, friend['email'], friend['firstname'], friend['lastname'])


