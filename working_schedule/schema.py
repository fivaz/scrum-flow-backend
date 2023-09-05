from datetime import time

from ninja import Schema


class WorkingScheduleSchema(Schema):
    start_at: time
    end_at: time


class NotFoundSchema(Schema):
    message: str
