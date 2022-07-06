from django.contrib.auth.models import User
from ninja import Router
from ninja.errors import HttpError

from api.auth.schemas import AccessToken, RegisterRequest, AuthRequest
from utils.security import create_access_token

router_auth = Router()


@router_auth.post(
    path="/register",
    response=AccessToken
)
def post_register(request, data: RegisterRequest):
    if User.objects.filter(email=data.email).exists():
        raise HttpError(400, "A user with such e-mail already exists.")

    user = User.objects.create_user(
        email=data.email,
        password=data.password,
        first_name=data.first_name,
        last_name=data.last_name
    )

    access_token = create_access_token(user.id)
    return AccessToken(access_token=access_token)


@router_auth.post(
    path="/auth",
    response=AccessToken
)
def post_auth(request, data: AuthRequest):
    user = User.objects.filter(email=data.email).first()
    if user and user.check_password(data.password):
        access_token = create_access_token(user.id)
        return AccessToken(access_token=access_token)
    raise HttpError(404, "There is no user with such email and password.")
