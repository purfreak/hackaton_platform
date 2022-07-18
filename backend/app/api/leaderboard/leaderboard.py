import datetime
from io import BytesIO

import pandas as pd

from ninja import Router, File
from ninja.files import UploadedFile
from ninja.errors import HttpError

from app.api.leaderboard.schemas import UploadSolutionResponse, GetLeaderboardResponse, LeaderboardData
from app.base.models import Team, TeamParticipant, Hackathon
from app.utils.dependency import AuthBearer

# from sklearn.metrics import f1_score

router_leaderboard = Router()


@router_leaderboard.post(
    path="/{hackathon_id}/upload_solution",
    auth=AuthBearer(),
    response=UploadSolutionResponse
)
def post_upload_solution(request, hackathon_id: int, team_id: int, file: UploadedFile = File(...)):
    team = Team.objects.filter(id=team_id).first()
    hackathon = Hackathon.objects.filter(id=hackathon_id).first()
    if not (hackathon.start_date <= datetime.datetime.now() <= hackathon.end_date):
        raise HttpError(400, "The hackathon has ended or hasn't started.")
    if not team:
        raise HttpError(404, "There is no team with such id.")
    if not TeamParticipant.objects.filter(user=request.auth, team=team).exists():
        raise HttpError(404, "You can not upload the solution.")

    submission = BytesIO(file.read())
    submission.seek(0)

    # score.py
    pred_labels = pd.read_csv(submission)
    true_labels = pd.read_csv('labels_test_dataset.csv')

    # team.score = f1_score(true_labels['Active'], pred_labels['Active'])
    # team.save()
    team.score = 0
    return UploadSolutionResponse(score=team.score)


@router_leaderboard.get(
    path="/{hackathon_id}",
    response=GetLeaderboardResponse
)
def get_leaderboard(request, hackathon_id: int):
    teams = Team.objects.filter(hackathon__id=hackathon_id).order_by('-score')
    leaderboard = []

    for team in teams:
        leaderboard.append(LeaderboardData(team_id=team.id, team_name=team.name, score=team.score))

    return GetLeaderboardResponse(leaderboard=leaderboard)
