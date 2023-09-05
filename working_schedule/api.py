from typing import List

from django.shortcuts import get_object_or_404
from ninja import NinjaAPI

from working_schedule.models import WorkingSchedule
from working_schedule.schema import WorkingScheduleSchema

api = NinjaAPI()


@api.get("/working-schedules", response=List[WorkingScheduleSchema])
def get(request):
    return WorkingSchedule.objects.all()


@api.get("/working-schedules/{working_schedule_id}", response=WorkingScheduleSchema)
def get(request, working_schedule_id: int):
    working_schedule = get_object_or_404(WorkingSchedule, id=working_schedule_id)
    return working_schedule


@api.post("/working-schedules", response={201: WorkingScheduleSchema})
def create(request, working_schedule: WorkingScheduleSchema):
    working_schedule = WorkingSchedule.objects.create(**working_schedule.dict())
    return working_schedule


@api.put("/working-schedules/{working_schedule_id}")
def update_employee(request, working_schedule_id: int, payload: WorkingScheduleSchema):
    working_schedule = get_object_or_404(WorkingSchedule, id=working_schedule_id)
    for attr, value in payload.dict().items():
        setattr(working_schedule, attr, value)
    working_schedule.save()
    return {"success": True}


@api.delete("/working-schedules/{working_schedule_id}")
def delete_employee(request, working_schedule_id: int):
    employee = get_object_or_404(WorkingSchedule, id=working_schedule_id)
    employee.delete()
    return {"success": True}
