from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password
from trip_calculator.imp.email_controler import EmailSender
from trip_calculator import models
import json
import secrets
import string


class CustomUserManager(BaseUserManager):
    def _create_user_in_DB_(self, email_address, firstname, lastname, password_hashed):
        if self.model is None:
            raise ValueError("Model has not been correctly set.")
        user = self.model(
            email=email_address,
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

    def get_by_user_id(self, email):
        return self.get_queryset().get(email=email).user_id

    def check_if_email_exists(self, email):
        return self.filter(email=email).exists()

    def register_user(self, email_address, firstname, lastname):
        if self.check_if_email_exists(email_address):
            return {"registration_pass": False}
        else:
            password = generate_random_password()
            password_hashed = make_password(password)
            self._create_user_in_DB_(email_address, firstname, lastname, password_hashed)
            send = EmailSender()
            send.set_email(email_address)
            send.set_password(password)
            send.generate_registration_message()
            send.send_email()
            return {"registration_pass": True}

    def invite_user(self, email_address):
        if self.check_if_email_exists(email_address):
            return {"registration_pass": False}
        else:
            password = generate_random_password()
            password_hashed = make_password(password)
            self._create_user_in_DB_(email_address, '-', '-', password_hashed)
            send = EmailSender()
            send.set_email(email_address)
            send.set_password(password)
            send.generate_invitation_message()
            send.send_email()
            return {"registration_pass": True}

    def recovery(self, email):
        if self.check_if_email_exists(email):
            new_password = generate_random_password()
            self._update_user_(self.get_by_user_id(email), password=new_password)
            recovery_message = EmailSender()
            recovery_message.set_email(email)
            recovery_message.generate_recovery_message()
            recovery_message.send_email()
            return {"recovery_pass": True}
        else:
            return {"recovery_pass": False}


def registration(data):
    return models.User.objects.register_user(data['email'], data['firstname'], data['lastname'])


def invite_user(data):
    data = json.loads(data['friend'])
    for user in data:
        models.User.objects.invite_user(user['email'])


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for i in range(length))
    return password