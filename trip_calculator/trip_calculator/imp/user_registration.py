from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from trip_calculator import models

from trip_calculator.imp import email_controler


class UserDetails:
    def __init__(self, email):
        self.email_address = email
        self.firstname = '-'
        self.lastname = '-'
        self.password = User.objects.make_random_password()
        self.password_hashed = make_password(self.password)

    def _create_user_in_DB_(self):
        create_user = models.User(
            password=self.password_hashed,
            firstname=self.firstname,
            lastname=self.lastname,
            email=self.email_address)
        create_user.save()

    def _update_user_(self, user_id, **kwargs):
        update_user = models.User.objects.get(id=user_id)

        if 'firstname' in kwargs != '':
            update_user.firstname = kwargs['firstname']

        if 'lastname' in kwargs != '':
            update_user.lastname = kwargs['lastname']

        if 'email' in kwargs != '':
            update_user.email = kwargs['email']

        if 'password' in kwargs != '':
            update_user.password = make_password(kwargs['password'])

        update_user.save()

    def _check_if_emailExist_(self):
        return models.User.objects.filter(email=self.email_address).exists()

    def get_user_id(self):
        user = models.User.objects.get(email=self.email_address)
        return user.user_id

    def set_user_details(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def set_password(self, password):
        self.password = password
        self.password_hashed = make_password(password)

    def set_email(self, email):
        self.email_address = email

    def register_user(self):
        if self._check_if_emailExist_():
            return {"registration_pass": False}
        else:
            self._create_user_in_DB_()
            invitation_message = email_controler.EmailSender()
            invitation_message.set_email(self.email_address)
            invitation_message.set_password(self.password)
            invitation_message.send_email()
            return {"registration_pass": True}

    def recovery(self, email):
        self.set_email(email)
        if self._check_if_emailExist_():
            new_password = User.objects.make_random_password()
            self._update_user_(self.get_user_id(),  password=new_password)
            recovery_message = email_controler.EmailSender()
            recovery_message.set_email(self.email_address)
            recovery_message.generate_recovery_message()
            recovery_message.send_email()
            return {"recovery_pass": True}
        else:
            return {"recovery_pass": False}


