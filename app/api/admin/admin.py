from django.contrib.auth.models import User
from ninja import Router, File
from ninja.files import UploadedFile
from ninja.errors import HttpError

from api.admin.schemas import GetTeamsResponse, TeamsData, GetTeamTeamParticipantsResponse, TeamParticipantData, \
    ResetPasswordRequest, MoveParticipantRequest, AddAdminsRequest
from base.models import Team, TeamParticipant, Hackathon
from utils.dependency import AuthBearerAdmin

router_admin = Router()


@router_admin.get(
    path="/teams",
    auth=AuthBearerAdmin(),
    response=GetTeamsResponse
)
def get_teams(request):
    teams = Team.objects.all()
    team_data = []

    for team in teams:
        team_data.append(TeamsData(id=team.id, name=team.name, hackathon_name=team.hackathon.id))
    return GetTeamsResponse(teams=team_data)


@router_admin.get(
    path="/teams/{team_id}/participants",
    auth=AuthBearerAdmin(),
    response=GetTeamTeamParticipantsResponse
)
def get_team_participants(request, team_id: int):
    team = Team.objects.filter(id=team_id).prefetch_related('participants').first()
    if not team:
        raise HttpError(404, "There is no team with such id.")
    team_participants_data = []

    for participant in team.participants.all():
        team_participants_data.append(TeamParticipantData(id=participant.user.id, first_name=participant.user.first_name,
                                                          last_name=participant.user.last_name,
                                                          email=participant.user.email,
                                                          role=participant.role))

    return GetTeamTeamParticipantsResponse(team_participants=team_participants_data)


@router_admin.put(
    path="/users/{user_id}/reset_password",
    auth=AuthBearerAdmin()
)
def put_reset_password(request, user_id: int, data: ResetPasswordRequest):
    user = User.objects.filter(id=user_id).first()
    if not user:
        raise HttpError(404, "There is no user with such id.")
    user.set_password(data.new_password)
    user.save()

    return


@router_admin.put(
    path="/teams/{team_id}/move",
    auth=AuthBearerAdmin()
)
def put_move_participant(request, team_id: int, data: MoveParticipantRequest):
    participant = TeamParticipant.objects.filter(user__id=data.user_id, team__id=team_id). \
        prefetch_related('team').first()

    if not participant:
        raise HttpError(404, "There is no such user in this team.")
    team = Team.objects.filter(id=data.team_arriving_id, hackathon__id=participant.team.hackathon.id).first()
    if not team:
        raise HttpError(404, "There is no such team to move the participant to.")

    TeamParticipant.objects.create(user=participant.user, role='T', team=team)
    participant.delete()

    return


@router_admin.delete(
    path="/teams/{team_id}/participants",
    auth=AuthBearerAdmin()
)
def delete_team_participant(request, team_id: int, user_id: int):
    participant = TeamParticipant.objects.filter(user__id=user_id, team__id=team_id).first()

    if not participant:
        raise HttpError(404, "There is no such user in this team.")

    participant.delete()

    return


@router_admin.put(
    path="/users/admin",
    auth=AuthBearerAdmin()
)
def put_add_admins(request, data: AddAdminsRequest):
    User.objects.filter(email__in=data.email_list).update(is_staff=True)

    return


@router_admin.put(
    path="{hackathon_id}/erase",
    auth=AuthBearerAdmin()
)
def put_erase_leaderboard(request, hackathon_id: int):
    if not Hackathon.objects.filter(id=hackathon_id).exists():
        raise HttpError(404, "There is no such hackathon.")
    teams = Team.objects.filter(hackathon__id=hackathon_id)
    for team in teams:
        team.score = 0
        team.save()


@router_admin.post(
    path="{hackathon_id}/files",
    # auth=AuthBearerAdmin()
)
def post_upload_files(request, hackathon_id: int, test_py: UploadedFile = File(...), train_py: UploadedFile = File(...),
                      labels_csv: UploadedFile = File(...)):
    hackathon = Hackathon.objects.filter(id=hackathon_id).first()
    if not hackathon:
        raise HttpError(404, "There is no such hackathon.")

    hackathon.test_py = test_py
    hackathon.train_py = train_py
    hackathon.labels_csv = labels_csv
    hackathon.save()
