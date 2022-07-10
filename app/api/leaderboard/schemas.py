from typing import List

from ninja import Schema


class UploadSolutionResponse(Schema):
    status: str
    score: int


class LeaderboardData(Schema):
    team_id: int
    team_name: str
    score: int


class GetLeaderboardResponse(Schema):
    leaderboard: List[LeaderboardData]