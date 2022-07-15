from django.contrib.auth.models import User
from ninja.security import HttpBearer

from utils.security import decode_access_token


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        decoded = decode_access_token(token)

        user_id = decoded.get('user_id')
        user_db = User.objects.filter(id=user_id).first()

        if user_db:
            return user_db

        raise Exception


class AuthBearerAdmin(HttpBearer):
    def authenticate(self, request, token):
        decoded = decode_access_token(token)
        user_id = decoded.get('user_id')
        user_db = User.objects.filter(id=user_id, is_staff=True).first()

        if user_db:
            return user_db

        raise Exception
