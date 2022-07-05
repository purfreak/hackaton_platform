import datetime
from io import BytesIO

import pandas as pd

from ninja import Router, File
from ninja.files import UploadedFile
from ninja.errors import HttpError

from api.leaderboard.schemas import UploadSolutionResponse, UploadSolutionRequest
from base.models import Team, TeamParticipant, Hackathon
from utils.dependency import AuthBearer
# from sklearn.metrics import f1_score

router_leaderboard = Router()


@router_leaderboard.post(
    path="/upload_solution",
    auth=AuthBearer(),
    response=UploadSolutionResponse
)
def post_upload_solution(request, data: UploadSolutionRequest, file: UploadedFile = File(...)):
    hackathon_id = Team.objects.filter(id=data.team_id).first.hackathon_id
    hackathon = Hackathon.objects.filter(id=hackathon_id).first
    if not (hackathon.start_date <= datetime.datetime.now() <= hackathon.end_date):
        raise HttpError(400, "The hackathon has ended or hasn't started.")

    if not Team.objects.filter(id=data.team_id).exists():
        raise HttpError(404, "There is no team with such id.")
    if not TeamParticipant.objects.filter(user=request.auth, team__id=data.team_id).exists():
        raise HttpError(404, "You can not upload the solution.")

    submission = BytesIO(file.read())
    submission.seek(0)

    # score.py
    pred_labels = pd.read_csv(submission)
    true_labels = pd.read_csv('labels_test_dataset.csv')

    # score = f1_score(true_labels['Active'], pred_labels['Active'])
    score = 0
    return UploadSolutionResponse(score=score)

# form the leaderboard

#get the leaderboard for the hackathon