import time
import requests
import random
import signal
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


STOCK_TYPES = ["AXA", "SGO", "SAP", "PKN", "LTS", "CDR", "ING", "PKO", "ZAP", "BDX"]


class TradeFillService:
    is_running = True

    def __init__(self, url: str = ""):
        self.url = url

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def stop(self, *args, **kwargs):
        logger.info("Stopping trade fill service...")
        self.is_running = False

    def interval(self) -> int:
        return random.randint(1, 3)

    def payload(self) -> dict:
        return {
            "stock_ticker": random.choice(STOCK_TYPES),
            "price": random.randint(10, 100),
            "quantity": random.randint(50, 150),
        }

    def run(self):
        with requests.Session() as s:
            while self.is_running:
                try:
                    s.post(url=self.url, json=self.payload())
                except Exception:
                    print("connection error")
                    pass
                time.sleep(self.interval())


if __name__ == "__main__":
    # TODO: from env
    t = TradeFillService(url="http://controller:8001/trade_fill/")
    t.run()
