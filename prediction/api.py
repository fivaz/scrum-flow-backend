from datetime import datetime, timezone
from typing import List

import requests
from ninja import Router
from sklearn.linear_model import LinearRegression

from prediction.models import Issue
from prediction.schema import IssueSchema, IssueInSchema
from schedule.api import BearerToken

router = Router()


@router.post("/", auth=BearerToken())
def create_issues(request, issues: List[IssueSchema]):
    for issue_data in issues:
        try:
            issue = Issue.objects.get(id=issue_data.id, user=request.auth)
            if issue_data.timeSpent == 0:
                issue.delete()
            else:
                Issue.objects.update(
                    id=issue_data.id,
                    defaults={
                        'estimation': issue_data.estimation,
                        'timeSpent': issue_data.timeSpent,
                        'completedDate': issue_data.completedDate,
                        'user': request.auth,
                    }
                )
        except Issue.DoesNotExist:
            if issue_data.timeSpent != 0:
                Issue.objects.create(
                    id=issue_data.id,
                    defaults={
                        'estimation': issue_data.estimation,
                        'timeSpent': issue_data.timeSpent,
                        'completedDate': issue_data.completedDate,
                        'user': request.auth,
                    }
                )
    return {"success": True}


def fetch_issues_backlog(board_id: int, access_token: str, cloud_id: str):
    url = f"https://api.atlassian.com/ex/jira/${cloud_id}"
    path = f"/rest/agile/1.0/board/${board_id}/backlog"
    query_params = f"?jql=issuetype%3DStory"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url + path + query_params, headers=headers)
    return response.json()


@router.post("/predict", response=List[IssueInSchema], auth=BearerToken())
def predict_issues(request, new_issues: List[IssueInSchema]):
    new_issues_with_estimation = [issue for issue in new_issues if issue.estimation is not None]

    issues = Issue.objects.filter(user=request.auth)

    new_issues_with_time_spent = make_predictions(issues, new_issues_with_estimation)
    return new_issues_with_time_spent


def make_predictions(issues: List[IssueSchema], new_issues: List[IssueInSchema]):
    # Prepare the data for training
    X_train = [[issue.estimation, (datetime.now(timezone.utc) - issue.completedDate).days] for issue in issues]

    y_train = [issue.timeSpent for issue in issues]

    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Now you can predict timeSpent for new issues
    new_X_test = [[issue.estimation, 0] for issue in new_issues]
    predictions = model.predict(new_X_test)

    for i in range(len(new_issues)):
        new_issues[i].timeSpent = predictions[i]

    return new_issues
