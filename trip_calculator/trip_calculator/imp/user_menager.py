from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)

    def get_user_by_id(self, user_id):
        return self.get(pk=user_id)