import logging
import blpapi
import time

from emsx_api_py.session_manager import SessionManager
from emsx_api_py.modules.demo_print_msg import DemoPrintMsg


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


HISTORY_SERVICE = "//blp/emsx.history"
EMAPISVC_BETA = "//blp/emapisvc_beta"


def main():

    manager = SessionManager()
    demo_mod = DemoPrintMsg()
    manager.register_module(demo_mod)

    # Synchronous start
    manager.start()
    session = manager.session

    # Synchronous open
    if not session.openService(EMAPISVC_BETA):
        logging.error(f"Failed to open service {EMAPISVC_BETA}")
    else:
        logging.info(f"Opened service {EMAPISVC_BETA}")

    # Subscribe

    # Draft subscription request
    topics = [
        "API_SEQ_NUM",
        "EMSX_ARRIVAL_PRICE",
        "EMSX_BROKER",
        "EMSX_TICKER",
        "EMSX_NOTES",
    ]
    subscription_topic = EMAPISVC_BETA + "/order?fields=" + ",".join(topics)

    subscriptions = blpapi.SubscriptionList()
    cid = blpapi.CorrelationId()
    subscriptions.add(topic=subscription_topic, correlationId=cid)

    logging.info("Subscribing to EMSX order updates...")
    session.subscribe(subscriptions)

    while True:
        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Program interrupted by user. Exiting...")