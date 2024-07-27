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
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('trip', 'user')


class Invitation(models.Model):
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)


class Cost(models.Model):
    cost_id = models.AutoField(primary_key=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    payer = models.ForeignKey(User, on_delete=models.CASCADE)
    cost_name = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2)



class Splited(models.Model):
    cost = models.ForeignKey(Cost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Friend(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend_of', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')
