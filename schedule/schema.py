from datetime import date, time
from typing import List

from ninja import Schema


class ScheduleSchema(Schema):
    id: str
    memberId: str
    startDate: date
    endDate: date
    startTime: time
    endTime: time
    daysOfWeek: List[int]
    isRecurring: bool


class ScheduleSchemaIn(Schema):
    memberId: str
    startDate: date
    endDate: date
    startTime: time
    endTime: time
    daysOfWeek: List[int]
    isRecurring: bool


class NotFoundSchema(Schema):
    message: str
