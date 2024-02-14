import requests

from config import settings
from utils.logger import logger


class HunterEmailVerifierClient:
    BASE_URL = settings.HUNTER_EMAIL_VERIFIER_BASE_URL

    def __init__(self, api_key: str):
        self.api_key = api_key

    def verify_email(self, email: str) -> dict:
        url = f"{self.BASE_URL}/email-verifier?email={email}&api_key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            response_json = response.json()
            logger.info(response_json)
            return response_json
        else:
            raise Exception(f"Failed to verify email: {response.content}")

    def get_email_status(self, email: str) -> str:
        data = self.verify_email(email).get("data", {})
        status = data.get("status", "accept_all")
        result = data.get("result", "risky")
        if result == "undeliverable":
            status = "invalid"
        return status

    def email_allowed(self, email: str) -> bool:
        return self.get_email_status(email) not in ["disposable", "invalid"]
