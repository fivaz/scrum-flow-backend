from typing import List

import requests
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from jiraone import LOGIN, endpoint
from ninja import NinjaAPI

from schedule.models import Schedule, User
from schedule.schema import ScheduleSchema, ScheduleSchemaIn

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


class JiraAccessToken1(HttpBearer):
    def authenticate(self, request, token):
        access_token = token.split(' ')
        return access_token[0]


@api.get("/schedule", response=List[ScheduleSchema], auth=JiraAccessToken())
def get(request):
    count = cache.get('data_route_count', 0)
    # Increment the count
    count += 1
    cache.set('data_route_count', count)
    print(f"This route has been called {count} times.")
    user = User.objects.get(cloudId=request.auth)
    schedules = Schedule.objects.filter(cloudId=user)
    return schedules.values()


@api.get("/schedule/{schedule_id}", response=ScheduleSchema, auth=JiraAccessToken())
def get(request, schedule_id: int):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    return schedule


@api.post("/schedule", response=ScheduleSchema, auth=JiraAccessToken())
def create(request, schedule: ScheduleSchemaIn):
    user, created = User.objects.get_or_create(cloudId=request.auth)

    schedule = Schedule.objects.create(
        cloudId=user,
        memberId=schedule.memberId,
        startDate=schedule.startDate,
        endDate=schedule.endDate,
        startTime=schedule.startTime,
        endTime=schedule.endTime,
        daysOfWeek=schedule.daysOfWeek,
        isRecurring=schedule.isRecurring,
    )
    return schedule


@api.put("/schedule/{schedule_id}", response=ScheduleSchema, auth=JiraAccessToken())
def update_employee(request, schedule_id: int, new_schedule: ScheduleSchemaIn):
    existing_schedule = get_object_or_404(Schedule, id=schedule_id)
    for attr, value in new_schedule.dict().items():
        setattr(existing_schedule, attr, value)
    existing_schedule.save()
    return existing_schedule


@api.delete("/schedule/{schedule_id}", auth=JiraAccessToken())
def delete_employee(request, schedule_id: int):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    schedule.delete()
    return {"success": True}


def fetch_data(token: str):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get('https://api.atlassian.com/oauth/token/accessible-resources', headers=headers)
    return response.json()


@api.get("/resources", auth=JiraAccessToken1())
def get_resources(request):
    # print(request.auth)
    count = cache.get('data_route_count', 0)
    # Increment the count
    count += 1
    cache.set('data_route_count', count)
    res = fetch_data(request.auth)
    print(res)
    print(f"This route has been called {count} times.")
    return res
