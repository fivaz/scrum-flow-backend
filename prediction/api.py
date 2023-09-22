from typing import List

from ninja import Router

from prediction.models import Issue
from prediction.schema import IssueSchema
from schedule.api import BearerToken

router = Router()


@router.post("/", auth=BearerToken())
def create_issues(request, issues: List[IssueSchema]):
    for issue_data in issues:
        issue, created = Issue.objects.update_or_create(
            id=issue_data.id,
            defaults={
                'key': issue_data.key,
                'summary': issue_data.summary,
                'estimation': issue_data.estimation,
                'timeSpent': issue_data.timeSpent,
                'completedDate': issue_data.completedDate,
                'user': request.auth,
            }
        )
    return {"success": True}
