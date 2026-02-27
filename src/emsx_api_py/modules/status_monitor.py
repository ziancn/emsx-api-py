"""
This module monitors general status like session status, services status, subscription status, etc.
"""

import blpapi
import logging

from .protocol import ModuleProtocol


# blpapi names
SLOW_CONSUMER_WARNING         = blpapi.Name("SlowConsumerWarning")
SLOW_CONSUMER_WARNING_CLEARED = blpapi.Name("SlowConsumerWarningCleared")

SESSION_STARTED               = blpapi.Name("SessionStarted")
SESSION_TERMINATED            = blpapi.Name("SessionTerminated")
SESSION_STARTUP_FAILURE       = blpapi.Name("SessionStartupFailure")
SESSION_CONNECTION_UP         = blpapi.Name("SessionConnectionUp")
SESSION_CONNECTION_DOWN       = blpapi.Name("SessionConnectionDown")

SERVICE_OPENED                = blpapi.Name("ServiceOpened")
SERVICE_OPEN_FAILURE          = blpapi.Name("ServiceOpenFailure")

SUBSCRIPTION_FAILURE          = blpapi.Name("SubscriptionFailure")
SUBSCRIPTION_STARTED          = blpapi.Name("SubscriptionStarted")
SUBSCRIPTION_TERMINATED       = blpapi.Name("SubscriptionTerminated")


class StatusMonitor(ModuleProtocol):
    """
    Logging module
    """
    def __init__(self):
        self._log_prefix = f"[{self.__class__.__name__}]"


    def process_event(
            self,
            event  : blpapi.Event,
            session: blpapi.Session,
    ):
        et = event.eventType()
        if   et == blpapi.Event.SESSION_STATUS      : self.process_session_status_event(event, session)
        elif et == blpapi.Event.SERVICE_STATUS      : self.process_service_status_event(event, session)
        elif et == blpapi.Event.SUBSCRIPTION_STATUS : self.process_subscription_status_event(event, session)
        elif et == blpapi.Event.ADMIN               : self.process_admin_event(event, session)
        else: pass


    def process_session_status_event(self, event: blpapi.Event, session: blpapi.Session):
        for msg in event:
            if   msg.messageType() == SESSION_STARTED         : logging.info(f"{self._log_prefix} Session started...")
            elif msg.messageType() == SESSION_STARTUP_FAILURE : logging.error(f"{self._log_prefix} Session startup failed")
            elif msg.messageType() == SESSION_CONNECTION_UP   : logging.info(f"{self._log_prefix} Session connection is up")
            elif msg.messageType() == SESSION_CONNECTION_DOWN : logging.info(f"{self._log_prefix} Session connection is down")
            elif msg.messageType() == SESSION_TERMINATED      : logging.info(f"{self._log_prefix} Session terminated")
            else: logging.info(f"{self._log_prefix} {msg}")


    def process_service_status_event(self, event: blpapi.Event, session: blpapi.Session):
        for msg in event:
            if   msg.messageType() == SERVICE_OPENED       : logging.info(f"{self._log_prefix} Service opened...")
            elif msg.messageType() == SERVICE_OPEN_FAILURE : logging.error(f"{self._log_prefix} Service failed to open")
            else: logging.info(f"{self._log_prefix} {msg}")


    def process_subscription_status_event(self, event: blpapi.Event, session: blpapi.Session):
        for msg in event:
            if   msg.messageType() == SUBSCRIPTION_STARTED    : logging.info(f"{self._log_prefix} Subscription started...")
            elif msg.messageType() == SUBSCRIPTION_FAILURE    : logging.error(f"{self._log_prefix} Subscription failed to start： {msg}")
            elif msg.messageType() == SUBSCRIPTION_TERMINATED : logging.error(f"{self._log_prefix} Subscription terminated")
            else: logging.info(f"{self._log_prefix} {msg}")


    def process_admin_event(self, event: blpapi.Event, session: blpapi.Session):
        for msg in event:
            if   msg.messageType() == SLOW_CONSUMER_WARNING         : logging.warning(f"{self._log_prefix} SLOW CONSUMER WARNING")
            elif msg.messageType() == SLOW_CONSUMER_WARNING_CLEARED : logging.info(f"{self._log_prefix} SLOW CONSUMER WARNING cleared")
            else: logging.info(f"{self._log_prefix} {msg}")