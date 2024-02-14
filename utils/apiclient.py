import requests
from fastapi_cache.decorator import cache
from requests import RequestException

from config import settings
from utils.logger import logger


class HunterEmailVerifierClient:
    BASE_URL = settings.HUNTER_EMAIL_VERIFIER_API_URL

    def __init__(self, api_key: str):
        self.api_key = api_key

    def verify_email(self, email: str) -> dict:
        try:
            url = f"{self.BASE_URL}/email-verifier?email={email}&api_key={self.api_key}"
            response = requests.get(url)
            response_json = response.json()
            if response.status_code > 400:
                logger.error(response_json)
                response_json = {}
        except RequestException as e:
            response_json = {}
            logger.error(e)

        logger.info(response_json)
        return response_json

    def get_email_status(self, email: str) -> str:
        result = self.verify_email(email)
        if result.get("errors"):
            return "disposable"

        data = result.get("data", {})

        result = data.get("result", "risky")
        if result == "undeliverable":
            return "invalid"

        status = data.get("status", "accept_all")
        return status

    @cache(expire=180)
    def email_allowed(self, email: str) -> bool:
        return self.get_email_status(email) not in ["disposable", "invalid"]
