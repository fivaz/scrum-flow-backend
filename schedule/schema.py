from datetime import datetime, time, date
from typing import List

from ninja import Schema

from schedule.models import User, Schedule


class RRuleSchema(Schema):
    freq: str = None
    byweekday: List[str] = None
    dtstart: datetime = None
    until: date = None


class ScheduleSchema(Schema):
    id: int
    memberId: str
    start: datetime = None
    end: datetime = None
    duration: time = None
    rrule: RRuleSchema = None


class ScheduleSchemaIn(Schema):
    memberId: str
    start: datetime = None
    end: datetime = None
    duration: time = None
    rrule: RRuleSchema = None


def model_to_schema(schedule: Schedule):
    return ScheduleSchema(
        id=schedule.id,
        memberId=schedule.memberId,
        start=schedule.start,
        end=schedule.end,
        duration=schedule.duration,
        rrule=RRuleSchema(
            freq=schedule.freq,
            byweekday=schedule.byweekday,
            dtstart=schedule.dtstart,
            until=schedule.until,
        ),
    )


def schema_to_model(schedule_in: ScheduleSchemaIn, user: User):
    schedule_obj = schedule_in.dict()
    rrule = schedule_obj.pop('rrule')
    if rrule is not None:
        model_dict = {**schedule_obj, **rrule, 'user': user}
    else:
        model_dict = {**schedule_obj, 'user': user}
    return model_dict
