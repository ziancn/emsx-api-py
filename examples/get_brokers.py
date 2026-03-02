"""
This example gets available brokers for a given asset class.
"""

import blpapi
import logging

from emsx_api_py.session_manager import SessionManager
from emsx_api_py.modules import StatusMonitor
from emsx_api_py.requests.buyside.get_brokers_with_asset_class import get_brokers_with_asset_class


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


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
    d_service = "//blp/emapisvc"
    session = session_manager.session
    session.openService(d_service)
    service_opened = session.getService(d_service)

    new_request = get_brokers_with_asset_class(
        service_opened,
        asset_class="EQTY"
    )

    def temp_handler(msg: blpapi.Message, session: blpapi.Session):
        print(msg)

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





