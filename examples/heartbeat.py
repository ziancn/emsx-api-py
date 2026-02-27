"""
This example subscribes and logs.
"""

import logging

from emsx_api_py.session_manager import SessionManager
from emsx_api_py.modules import DemoModule, StatusMonitor


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
    demo_module = DemoModule()      # Demo that subscribes and logs heartbeat
    # Register modules
    session_manager.register_module(status_mon)
    session_manager.register_module(demo_module)

    # Start
    session_manager.start_async()

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

