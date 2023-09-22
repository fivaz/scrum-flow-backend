from datetime import datetime

from ninja import Schema


class IssueSchema(Schema):
    id: int
    key: str
    summary: str
    estimation: float
    timeSpent: int
    completedDate: datetime
