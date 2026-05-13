import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from dotenv import load_dotenv
from pathlib import Path

# Load .env file
env_path = Path(r"D:\FastAPI Projects\incident-ops-system\backend\.env")
load_dotenv(dotenv_path=env_path)

# Read environment variables
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL")

# Create email
message = Mail(
    from_email=FROM_EMAIL,
    to_emails="khansaimon695@gmail.com",
    subject="IncidentOps Email Test",
    plain_text_content="Critical incident detected in production."
)

try:
    # Send email
    sg = SendGridAPIClient(SENDGRID_API_KEY)

    response = sg.send(message)

    print("Status Code:", response.status_code)
    print("Response Body:", response.body)
    print("Headers:", response.headers)

except Exception as e:
    print("Error:", str(e))