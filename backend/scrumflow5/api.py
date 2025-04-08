from ninja import NinjaAPI

from backend.prediction.api import router as issue_router
from backend.schedule.api import router as schedule_router

api = NinjaAPI()

api.add_router("/schedules/", schedule_router)
api.add_router("/issues/", issue_router)

# Health check route
@api.get("/health")
def health_check(request):
    return {"status": "ok"}