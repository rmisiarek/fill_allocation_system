from typing import Optional, List
from threading import Thread
import time
import requests
import random
import signal
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


STOCK_TYPES = ["AXA", "SGO", "SAP", "PKN", "LTS", "CDR", "ING", "PKO", "ZAP", "BDX"]


class AUMService:
    is_running = True

    def __init__(self, url: str = ""):
        self.url = url

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def stop(self, *args, **kwargs):
        logger.info("Stopping AUM service...")
        self.is_running = False

    def interval(self) -> int:
        return 30

    def create_payload(self, *, accounts_number: int) -> dict:
        result = []
        percentage = 100
        for idx, data in enumerate(range(1, accounts_number)):
            if percentage == 0:
                break

            random_percentage = random.randint(1, percentage)
            percentage = percentage - random_percentage
            result.append(
                self.create_account_payload(
                    account_id=idx + 1, percentage=random_percentage
                )
            )

        result.append(
            self.create_account_payload(
                account_id=accounts_number, percentage=percentage
            )
        )

        return result

    def create_account_payload(self, *, account_id: int, percentage: int) -> dict:
        return {
            "account_name": f"Account_{account_id}",
            "percentage": percentage,
        }

    def run(self):
        with requests.Session() as s:
            while self.is_running:
                payload = {
                    "data": self.create_payload(accounts_number=random.randint(1, 5))
                }
                try:
                    s.post(url=self.url, json=payload)
                except Exception:
                    print("connection error")
                    pass
                time.sleep(self.interval())


if __name__ == "__main__":
    # TODO: from env
    t = AUMService(url="http://controller:8001/assets_distribution/")
    t.run()
