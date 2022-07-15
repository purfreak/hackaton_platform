from datetime import datetime
from typing import List

from ninja import Schema
from pydantic import EmailStr, AnyHttpUrl


class HackathonsData(Schema):
    id: int
    name: str
    start_time: datetime
    end_time: datetime


class HackathonsResponse(Schema):
    hackathons: List[HackathonsData]


class CreateTeamRequest(Schema):
    name: str
    email_list: List[EmailStr]


class AddRepositoryRequest(Schema):
    url: AnyHttpUrl
