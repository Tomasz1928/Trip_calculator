from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password
from trip_calculator.imp.email_controller import EmailSender
import json, secrets, string


def get_user_model():
    from trip_calculator.models import User
    return User

class CustomUserManager(BaseUserManager):
    def _create_user_in_DB_(self, email, firstname, lastname, password_hashed):
        if not email:
            raise ValueError("The Email field must be set")
        user = self.model(
            email=email,
            firstname=firstname,
            lastname=lastname,
            password=password_hashed
        )
        user.save(using=self._db)
        return user

    def _update_user_(self, user_id, **kwargs):
        update_user = self.get_queryset().get(user_id=user_id)

        if 'firstname' in kwargs and kwargs['firstname']:
            update_user.firstname = kwargs['firstname']

        if 'lastname' in kwargs and kwargs['lastname']:
            update_user.lastname = kwargs['lastname']

        if 'email' in kwargs and kwargs['email']:
            update_user.email = kwargs['email']

        if 'password' in kwargs and kwargs['password']:
            update_user.password = make_password(kwargs['password'])

        update_user.save(using=self._db)

    def get_by_natural_key(self, email):
        return self.get_queryset().get(email=email)

    def get_user_id_by_email(self, email):
        return self.get_queryset().get(email=email).user_id

    def get_user_by_id(self, user_id):
        print(user_id)
        return self.get_queryset().get(user_id=user_id)

    def check_if_email_exists(self, email):
        return self.filter(email=email).exists()

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
        from trip_calculator.imp.friend_controller import FriendController
        if self.check_if_email_exists(email):
            friend_id = self.get_user_id_by_email(email)
            new_friend = FriendController(user_id)
            new_friend.add_friend(friend_id)
            return {"registration_pass": False}
        else:
            password = generate_random_password()
            password_hashed = make_password(password)
            self._create_user_in_DB_(email, firstname, lastname, password_hashed)

            new_friend = FriendController(user_id)
            new_friend.add_friend(self.get_user_id_by_email(email))

            send = EmailSender()
            send.set_email(email)
            send.set_password(password)
            send.generate_invitation_message()
            send.send_email()
            return {"registration_pass": True}

    def recovery(self, email):
        if self.check_if_email_exists(email):
            user = self.get_by_natural_key(email)
            new_password = generate_random_password()
            self._update_user_(user.user_id, password=new_password)
            recovery_message = EmailSender()
            recovery_message.set_email(email)
            recovery_message.set_password(new_password)
            recovery_message.generate_recovery_message()
            recovery_message.send_email()
            return {"recovery_pass": True}
        else:
            return {"recovery_pass": False}


def registration(data):
    user = get_user_model()
    return user.objects.register_user(data['email'], data['firstname'], data['lastname'])


def recovery(data):
    user = get_user_model()
    return user.objects.recovery(data['email'])


def get_user_infor(user_id):
    user = get_user_model()
    data = user.objects.get(user_id=user_id)
    return {'name': data.firstname, 'lastname': data.lastname, 'email': data.email, 'added': data.created_at.strftime("%d.%m.%Y"), 'user_id': user_id}


def invite_user(user_id, data):
    user = get_user_model()
    friends_data = json.loads(data['friend'])
    for friend in friends_data:
        user.objects.invite_user(user_id, friend['email'], friend['firstname'], friend['lastname'])


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password