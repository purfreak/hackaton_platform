from django.contrib.auth.models import User
from ninja import Router
from ninja.errors import HttpError

from api.users.schemas import MeResponse, PassChangeStatus, ChangePassRequest, GetTeamInvitesResponse, InviteList, \
    PostTeamInvitesRequest
from base.models import TeamParticipant
from utils.dependency import AuthBearer

router_users = Router()


@router_users.get(
    path="/me",
    auth=AuthBearer(),
    response=MeResponse
)
def get_me(request):
    return MeResponse(first_name=request.auth.first_name, last_name=request.auth.last_name, email=request.auth.email)


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


@router_users.get(
    path="/teams/invites",
    auth=AuthBearer(),
    response=GetTeamInvitesResponse
)
def get_team_invites(request):
    user = request.auth
    invites = []
    list_of_invites = TeamParticipant.objects.filter(user=user, role='I')
    for element in list_of_invites:
        invites.append(InviteList(team_name=element.team.name,
                                  hackathon_name=element.team.hackathon.name,
                                  start_date=element.team.hackathon.start_time,
                                  end_date=element.team.hackathon.end_time))

    return GetTeamInvitesResponse(invites=invites)


@router_users.post(
    path="/teams/invite",
    auth=AuthBearer()
)
def post_team_invites(request, data: PostTeamInvitesRequest):
    if data.status == PostTeamInvitesRequest.InviteEnum.accepted:
        user = TeamParticipant.objects.filter(user=request.auth, team__id=data.team_id).first()
        user.role = 'T'
        user.save()

    if data.status == PostTeamInvitesRequest.InviteEnum.declined:
        user = TeamParticipant.objects.filter(user=request.auth, team__id=data.team_id).first()
        user.role = 'D'
        user.save()

    return
