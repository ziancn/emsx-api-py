"""
This example gets historical fills.
"""

import blpapi
import logging

from zoneinfo import ZoneInfo
from datetime import datetime

from emsx_api_py.session_manager import SessionManager
from emsx_api_py.modules import StatusMonitor
from emsx_api_py.requests.buyside import get_fills


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


GET_FILLS_RESPONSE = blpapi.Name("GetFillsResponse")
FILLS = blpapi.Name("Fills")


def main():
    # Session manager instance
    session_manager = SessionManager()
    # Modules
    status_mon = StatusMonitor()    # Log status related event/message
    # Register modules
    session_manager.register_module(status_mon)

    # Start
    session_manager.start()

    # Request and Response handler
    d_service = "//blp/emsx.history"
    session = session_manager.session
    session.openService(d_service)
    service_opened = session.getService(d_service)

    # Compose request
    seoul_tz = ZoneInfo("Asia/Seoul")
    start_dt = datetime(2026,3,10,9,0,0, tzinfo=seoul_tz)
    end_dt = datetime(2026,3,10,9,1,0, tzinfo=seoul_tz)

    new_request = get_fills(
        service_opened,
        start_dt = start_dt.isoformat(timespec="milliseconds"),
        end_dt = end_dt.isoformat(timespec="milliseconds"),
        scope_choice="Team",
        team_name="CITICHK"
    )

    def temp_handler(msg: blpapi.Message, session: blpapi.Session):
        if msg.messageType() != GET_FILLS_RESPONSE:
            return

        fills = msg.getElement(FILLS)

        for fill in fills.values():
            exchange = fill.getElement("Exchange").getValueAsString()
            if exchange != "KS": continue

            ticker = fill.getElement("Ticker").getValueAsString()
            side = fill.getElement("Side").getValueAsString()
            fillId = fill.getElement("FillId").getValueAsInteger()
            fillPrice = fill.getElement("FillPrice").getValueAsFloat()
            fillShares = fill.getElement("FillShares").getValueAsFloat()

            print(
                f"{ticker} {side} order fill: {fillShares}shs @ {fillPrice} (ID: {fillId})\n"
            )


    # Send request
    session_manager.send_request(new_request, temp_handler)

    # Block main thread
    try:
        print("Press ENTER to quit")
        input()
    finally:
        session_manager.session.stop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Stopped by user")





