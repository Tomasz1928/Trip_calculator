from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from trip_calculator.imp.registration_controller import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Trip(models.Model):
    trip_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    start = models.CharField(max_length=255)
    end = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class UserTrip(models.Model):
    trip_id = models.IntegerField()
    user_id = models.IntegerField()


class Invitation(models.Model):
    email = models.EmailField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)


class Cost(models.Model):
    cost_id = models.AutoField(primary_key=True)
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE)
    payer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    cost_name = models.CharField(max_length=255)
    value = models.IntegerField()


class Splited(models.Model):
    cost_id = models.ForeignKey(Cost, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Friend(models.Model):
    user_id = models.IntegerField()
    friend_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
