from ninja import Schema
from typing import List

from pydantic import EmailStr, validator


class TeamsData(Schema):
    id: int
    name: str
    hackathon_name: str


class GetTeamsResponse(Schema):
    teams: List[TeamsData]


class TeamParticipantData(Schema):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: str


class GetTeamTeamParticipantsResponse(Schema):
    team_participants: List[TeamParticipantData]


class ResetPasswordRequest(Schema):
    new_password: str

    @validator("new_password", allow_reuse=True)
    def check_password_len(cls, new_password):
        if len(new_password) < 6:
            raise ValueError("The password should be at least 6 characters long")

        return new_password


class MoveParticipantRequest(Schema):
    user_id: int
    team_arriving_id: int
