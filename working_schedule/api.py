from typing import List

from django.shortcuts import get_object_or_404
from jiraone import LOGIN, endpoint
from ninja import NinjaAPI

from working_schedule.models import WorkingSchedule
from working_schedule.schema import WorkingScheduleSchema

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


@api.get("/working-schedule", response=List[WorkingScheduleSchema], auth=JiraAccessToken())
def get(request):
    working_schedule = get_object_or_404(WorkingSchedule, cloud_id=request.auth)
    return working_schedule


@api.post("/working-schedule", response=WorkingScheduleSchema, auth=JiraAccessToken())
def create(request, payload: WorkingScheduleSchema):
    working_schedule, created = WorkingSchedule.objects.update_or_create(cloud_id=request.auth, defaults={
        "start_at": payload.start_at,
        "end_at": payload.end_at
    })
    return working_schedule
