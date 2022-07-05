from django.contrib.auth.models import User
from ninja import Router
from ninja.errors import HttpError

from api.users.schemas import MeResponse, PassChangeStatus, ChangePassRequest
from utils.dependency import AuthBearer

router_users = Router()


@router_users.get(
    path="/me",
    response=MeResponse
)
def get_me(request, user_id: int):
    users = User.objects.filter(id=user_id)
    if not users.exists():
        raise HttpError(404, "A user with such id wasn't found.")
    return users.first()


@router_users.post(
    path="/change_password",
    auth=AuthBearer(),
    response=PassChangeStatus
)
def post_change_pass(request, data: ChangePassRequest):
    if request.auth.check_password(data.password):
        request.auth.set_password(data.new_password)
        request.auth.save()
        return PassChangeStatus(status="Password changed successfully.")
    return PassChangeStatus(status="Something went wrong.")
