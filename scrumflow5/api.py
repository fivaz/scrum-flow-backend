from ninja import NinjaAPI

from prediction.api import router as issue_router
from schedule.api import router as schedule_router

api = NinjaAPI()

api.add_router("/schedules/", schedule_router)
api.add_router("/issues/", issue_router)
