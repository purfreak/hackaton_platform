from datetime import datetime
from enum import Enum
from typing import List

from ninja import Schema
from pydantic import validator, EmailStr


class MeResponse(Schema):
    first_name: str
    last_name: str
    email: EmailStr


class PassChangeStatus(Schema):
    status: str


class ChangePassRequest(Schema):
    password: str
    new_password: str

    @validator("new_password", allow_reuse=True)
    def check_password_len(cls, new_password):
        if len(new_password) < 6:
            raise ValueError("The password should be at least 6 characters long")

        return new_password


class InviteList(Schema):
    team_name: str
    hackathon_name: str
    start_date: datetime
    end_date: datetime


class GetTeamInvitesResponse(Schema):
    invites: List[InviteList]


class PostTeamInvitesRequest(Schema):
    class InviteEnum(str, Enum):
        accepted = 'accepted'
        declined = 'declined'

    team_id: int
    status: InviteEnum

