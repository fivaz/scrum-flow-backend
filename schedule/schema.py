from datetime import time

from ninja import Schema


class ScheduleSchema(Schema):
    start_at: time
    end_at: time


class NotFoundSchema(Schema):
    message: str
