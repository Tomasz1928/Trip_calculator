from django.db import models


class Trip(models.Model):
    tabel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    start = models.CharField(max_length=255)
    end = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class UserTrip(models.Model):
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


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
