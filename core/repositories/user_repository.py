from django.contrib.auth.models import make_password
from django.db import IntegrityError
from core.models import User
from v0.errors.app_error import App_Error


class User_Repository():
    def get_or_create_user(self, data):
        try:
            return User.objects.get_or_create(name=data["name"], last_name=data["last_name"], birth_date=data["birth_date"], email=data["email"], state=data["state"], username=data["username"], cellphone=data["cellphone"], defaults={"password": make_password(data["password"])})

        except IntegrityError as e:
            raise App_Error(
                f'INTEGRITY_ERROR USER_REPOSITORY_CREATE_USER {str(e)}', 500)

    def create_user(self, data):
        try:
            return User.objects.create(**data)

        except IntegrityError as e:
            raise App_Error(
                f'INTEGRITY_ERROR USER_REPOSITORY_CREATE_USER {str(e)}', 500)

    def find_user(self, data):
        try:
            return User.objects.get(**data)
        except User.DoesNotExist:
            return None
