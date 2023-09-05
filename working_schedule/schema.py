from datetime import time

from ninja import Schema


class WorkingScheduleSchema(Schema):
    start_at: time
    end_at: time
    cloud_id: int


class NotFoundSchema(Schema):
    message: str
