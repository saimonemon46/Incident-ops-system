from pathlib import Path
from dotenv import load_dotenv
import os
import requests

env_path = Path(r"D:\FastAPI Projects\incident-ops-system\backend\.env")

load_dotenv(dotenv_path=env_path)

url = os.getenv("SLACK_WEBHOOK_URL")

payload = {
    "text": "Test message from Python"
}

response = requests.post(
    url,
    json=payload
)

print(response.status_code)
print(response.text)