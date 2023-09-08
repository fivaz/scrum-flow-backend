from django.shortcuts import get_object_or_404
from jiraone import LOGIN, endpoint
from ninja import NinjaAPI

from schedule.models import Schedule
from schedule.schema import ScheduleSchema

api = NinjaAPI()

from ninja.security import HttpBearer


class JiraAccessToken(HttpBearer):
    def authenticate(self, request, token):
        [access_token, cloud_id] = token.split(' ')
        LOGIN.base_url = f"https://api.atlassian.com/ex/jira/{cloud_id}"
        LOGIN.token_session(sess=access_token)

        response = LOGIN.get(endpoint.myself())

        if response.status_code == 200:
            return cloud_id


@api.get("/schedule", response=ScheduleSchema, auth=JiraAccessToken())
def get(request):
    schedule = get_object_or_404(Schedule, cloud_id=request.auth)
    return schedule


@api.get("/schedule/{schedule_id}", response=ScheduleSchema)
def get(request, schedule_id: int):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    return schedule


# @api.post("/schedule", response=ScheduleSchema, auth=JiraAccessToken())
# def create(request, schedule: ScheduleSchema):
#     schedule = Schedule.objects.create(cloud_id=request.auth, defaults={
#         id: string;
#         employeeId: string;
#         startDate: string;
#         endDate: string;
#         startTime: string;
#         endTime: string;
#         daysOfWeek: number[];
#         isRecurring: boolean;
#     })
#     return schedule


@api.post("/schedule", response=ScheduleSchema, auth=JiraAccessToken())
def create(request, payload: ScheduleSchema):
    schedule, created = Schedule.objects.update_or_create(cloud_id=request.auth, defaults={
        "start_at": payload.start_at,
        "end_at": payload.end_at
    })
    return schedule


@api.put("/schedule/{schedule_id}")
def update_employee(request, schedule_id: int, payload: ScheduleSchema):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    for attr, value in payload.dict().items():
        setattr(schedule, attr, value)
    schedule.save()
    return {"success": True}


@api.delete("/schedule/{schedule_id}")
def delete_employee(request, schedule_id: int):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    schedule.delete()
    return {"success": True}
