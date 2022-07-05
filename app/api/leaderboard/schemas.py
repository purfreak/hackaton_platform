from ninja import Schema


class UploadSolutionRequest(Schema):
    team_id: int


class UploadSolutionResponse(Schema):
    status: str
    score: int
