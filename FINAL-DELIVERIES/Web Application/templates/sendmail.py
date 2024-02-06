import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email="nithishkumarsivan@gmail.com",
    to_emails=("bkprem9296@gmail.com", "prembaskargovindharaj@gmail.com"),
    subject="CONTAINMENT ZONE APP",
    html_content="<strong>and easy to do anywhere, even with Python</strong>")
try:
    sg = SendGridAPIClient(os.environ.get("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"))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)