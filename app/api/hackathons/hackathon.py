from django.contrib.auth.models import User
from ninja import Router
from ninja.errors import HttpError

from api.hackathons.schemas import HackathonsResponse, HackathonsData, CreateTeamRequest, AddRepositoryRequest
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
    auth=AuthBearer()
)
def post_choose_hackathon(request, hackathon_id: int):
    hackathon = Hackathon.objects.filter(id=hackathon_id).first()
    if not hackathon:
        raise HttpError(404, "There is no hackathon with such id.")
    if HackathonParticipant.objects.filter(user=request.auth, hackathon=hackathon).exists():
        raise HttpError(400, "This user has already registered for this hackathon.")

    HackathonParticipant.objects.create(user=request.auth, hackathon=hackathon)

    return


@router_hackathons.post(
    path="/teams/{hackathon_id}/create",
    auth=AuthBearer()
)
def post_create_team(request, hackathon_id: int, data: CreateTeamRequest):
    if Team.objects.filter(name=data.name).exists():
        raise HttpError(400, "A team with such name already exists. Please choose a different name.")
    if TeamParticipant.objects.filter(user=request.auth, team__hackathon__id=hackathon_id).exists():
        raise HttpError(400, "You have already chosen your team for this hackathon.")

    new_team = Team.objects.create(name=data.name, hackathon__id=hackathon_id)
    TeamParticipant.objects.create(user=request.auth, role='C', team=new_team)

    for element in data.email_list:
        user = User.objects.filter(email=element)
        if TeamParticipant.objects.filter(user__email=element, team__hackathon__id=hackathon_id).exists():
            raise HttpError(400, f"This user {element} has already chosen their team for this hackathon.")
        if not HackathonParticipant.objects.filter(user__email=element, hackathon__id=hackathon_id).exists():
            TeamParticipant.objects.create(user=user, role='I', team=new_team)
        else:
            raise HttpError(400, f"This user {element} hasn't chosen this hackathon.")

    return


@router_hackathons.post(
    path="/teams/{hackathon_id}/repository",
    auth=AuthBearer()
)
def post_add_repository(request, hackathon_id: int, data: AddRepositoryRequest):
    captain_query = TeamParticipant.objects.filter(user=request.auth, team__hackathon__id=hackathon_id, role='C')
    if captain_query.exists():
        captain = captain_query.first()
        captain.team.url = data.url
        captain.save()
    else:
        raise HttpError(400, "You do not have access to adding the repository.")
    return


