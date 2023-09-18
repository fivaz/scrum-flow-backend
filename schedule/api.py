from typing import List

import requests
from django.core.cache import cache
from jiraone import LOGIN, endpoint
from ninja import NinjaAPI
from ninja.security import HttpBearer

from schedule.models import Schedule, User
from schedule.schema import ScheduleSchema, model_to_schema, ScheduleSchemaIn, schema_to_model

api = NinjaAPI()


def check_token_validity(token: str):
    [access_token, cloud_id] = token.split(' ')
    LOGIN.base_url = f"https://api.atlassian.com/ex/jira/{cloud_id}"
    LOGIN.token_session(sess=access_token)

    response = LOGIN.get(endpoint.myself())

    if response.status_code == 200:
        return cloud_id


class BearerToken(HttpBearer):
    def authenticate(self, request, token):
        cloud_id = check_token_validity(token)
        if cloud_id:
            user, created = User.objects.get_or_create(cloudId=cloud_id)
            return user


class JiraAccessToken(HttpBearer):
    def authenticate(self, request, token):
        access_token = token.split(' ')
        return access_token[0]


@api.get("/schedules", response=List[ScheduleSchema], auth=BearerToken())
def get_schedules(request):
    schedules = Schedule.objects.filter(user=request.auth)
    # return schedules
    return [model_to_schema(schedule) for schedule in schedules]


@api.get("/schedules/{schedule_id}", response=ScheduleSchema, auth=BearerToken())
def get_schedule(request, schedule_id: int):
    schedule = Schedule.objects.get(id=schedule_id, user=request.auth)
    return model_to_schema(schedule)


@api.post("/schedules", auth=BearerToken())
def create_schedule(request, schedule_in: ScheduleSchemaIn):
    schedule_obj = schema_to_model(schedule_in, request.auth)
    schedule = Schedule.objects.create(**schedule_obj)
    return model_to_schema(schedule)


@api.put("/schedules/{schedule_id}", response=ScheduleSchema, auth=BearerToken())
def update_schedule(request, schedule_id: int, schedule_in: ScheduleSchemaIn):
    schedule = Schedule.objects.get(id=schedule_id, user=request.auth)
    new_schedule_obj = schema_to_model(schedule_in, request.auth)
    for attr, value in new_schedule_obj.items():
        setattr(schedule, attr, value)
    schedule.save()
    return model_to_schema(schedule)


@api.delete("/schedules/{schedule_id}", auth=BearerToken())
def delete_schedule(request, schedule_id: int):
    schedule = Schedule.objects.get(id=schedule_id, user=request.auth)
    schedule.delete()
    return {"success": True}


def fetch_data(token: str):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get('https://api.atlassian.com/oauth/token/accessible-resources', headers=headers)
    return response.json()


@api.get("/resources", auth=JiraAccessToken())
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
