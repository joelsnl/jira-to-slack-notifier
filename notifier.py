import requests
import json

# Configs
JIRA_URL = "https://your-domain.atlassian.net/rest/api/2/search"
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/your/webhook/url"
JIRA_AUTH = ("your-email", "your-api-token")

def get_open_jira_tickets():
    query = {"jql": "assignee=currentUser() AND status!=Done", "maxResults": 5}
    response = requests.get(JIRA_URL, auth=JIRA_AUTH, params=query)
    response.raise_for_status()
    return response.json()["issues"]

def send_to_slack(issues):
    text = "\n".join([f"- {issue['key']}: {issue['fields']['summary']}" for issue in issues])
    payload = {"text": f"🛠️ Open Jira Tickets:\n{text}"}
    requests.post(SLACK_WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    tickets = get_open_jira_tickets()
    send_to_slack(tickets)
