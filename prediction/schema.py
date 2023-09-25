from datetime import datetime

from ninja import Schema


class IssueSchema(Schema):
    isUsed: bool
    id: str
    estimation: float
    timeSpent: int
    completedDate: datetime


class IssueInSchema(Schema):
    id: str
    estimation: float = None
    timeSpent: int
