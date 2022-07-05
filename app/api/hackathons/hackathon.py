from django.contrib.auth.models import User
from ninja import Router
from ninja.errors import HttpError

from api.hackathons.schemas import HackathonsResponse, HackathonsData, ChooseHackathonResponse, ChooseHackathonRequest, \
    MakeTeamResponse, MakeTeamRequest, AddRepositoryResponse, AddRepositoryRequest, GetTeamInvitesResponse, InviteList, \
    PostTeamInvitesRequest
from base.models import Hackathon, HackathonParticipant, Team, TeamParticipant
from utils.dependency import AuthBearer

router_hackathons = Router()


@router_hackathons.get(
    path="",
    response=HackathonsResponse
)
def get_hackathons(request):
    hackathons = Hackathon.objects.all()
    hackathon_data = []
    for element in hackathons:
        hackathon_data.append(
            HackathonsData(id=element.id, name=element.name, start_time=element.start_time, end_time=element.end_time))
    return HackathonsResponse(hackathons=hackathon_data)


@router_hackathons.post(
    path="/choose",
    auth=AuthBearer(),
    response=ChooseHackathonResponse
)
def post_choose_hackathon(request, data: ChooseHackathonRequest):
    if not Hackathon.objects.filter(id=data.hackathon_id).exists():
        raise HttpError(404, "There is no hackathon with such id.")
    if HackathonParticipant.objects.filter(user=request.auth, hackathon_id=data.hackathon_id).exists():
        raise HttpError(400, "This user has already registered for this hackathon.")

    HackathonParticipant.objects.create(user=request.auth, hackathon_id=data.hackathon_id)

    return ChooseHackathonResponse(status=200)


@router_hackathons.post(
    path="/teams",
    auth=AuthBearer(),
    response=MakeTeamResponse
)
def post_make_team(request, data: MakeTeamRequest):
    if Team.objects.filter(name=data.name).exists():
        raise HttpError(400, "A team with such name already exists. Please choose a different name.")
    if TeamParticipant.objects.filter(user=request.auth, team__hackathon__id=data.hackathon_id).exists():
        raise HttpError(400, "You have already chosen your team for this hackathon.")

    new_team = Team.objects.create(name=data.name, hackathon_id=data.hackathon_id)
    TeamParticipant.objects.create(user=request.auth, role='C', team=new_team)

    for element in data.email_list:
        user = User.objects.filter(email=element)
        if TeamParticipant.objects.filter(user__email=element, team__hackathon__id=data.hackathon_id).exists():
            raise HttpError(400, f"This user {element} has already chosen their team for this hackathon.")
        if not HackathonParticipant.objects.filter(user__email=element, hackathon__id=data.hackathon_id).exists():
            TeamParticipant.objects.create(user=user, role='I', team=new_team)
        else:
            raise HttpError(400, f"This user {element} hasn't chosen this hackathon.")

    return MakeTeamResponse(status="The team was successfully made.")


@router_hackathons.post(
    path="/teams/repository",
    auth=AuthBearer(),
    response=AddRepositoryResponse
)
def post_add_repository(request, data: AddRepositoryRequest):
    captain_query = TeamParticipant.objects.filter(user=request.auth, team__hackathon__id=data.hackathon_id, role='C')
    if captain_query.exists():
        captain = captain_query.first()
        captain.team.url = data.url
        captain.save()
    else:
        raise HttpError(400, "You do not have access to adding the repository.")


@router_hackathons.get(
    path="/teams/invites",
    auth=AuthBearer(),
    response=GetTeamInvitesResponse
)
def get_team_invites(request):
    user = request.auth
    invites = []
    list_of_invites = TeamParticipant.objects.filter(user=user, role='I')
    for element in list_of_invites:
        invites.append(InviteList(team=element.team.name,
                                  hackathon=element.team.hackathon.name,
                                  start_date=element.team.hackathon.start_time,
                                  end_date=element.team.hackathon.end_time))

    return GetTeamInvitesResponse(invites=invites)


@router_hackathons.post(
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
