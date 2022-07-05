from datetime import datetime
from typing import List
from enum import Enum

from ninja import Schema
from pydantic import EmailStr, AnyHttpUrl


class HackathonsData(Schema):
    id: int
    name: str
    start_time: datetime
    end_time: datetime


class HackathonsResponse(Schema):
    hackathons: List[HackathonsData]


class ChooseHackathonRequest(Schema):
    hackathon_id: int


class ChooseHackathonResponse(Schema):
    status: str


class MakeTeamRequest(Schema):
    name: str
    hackathon_id: int
    email_list: List[EmailStr]


class MakeTeamResponse(Schema):
    status: str


class AddRepositoryRequest(Schema):
    url: AnyHttpUrl
    hackathon_id: int


class AddRepositoryResponse(Schema):
    status: str


class InviteList(Schema):
    team: str
    hackathon: str
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

