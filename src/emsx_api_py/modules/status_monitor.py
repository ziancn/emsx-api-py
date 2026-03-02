"""
This module monitors general status like session status, services status, subscription status, etc.
"""

import blpapi
import logging

from .protocol import ModuleProtocol


# blpapi names
class SessionMsg:
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
        match event.eventType():
            case blpapi.Event.SESSION_STATUS      : self.process_session_status_event(event, session)
            case blpapi.Event.SERVICE_STATUS      : self.process_service_status_event(event, session)
            case blpapi.Event.SUBSCRIPTION_STATUS : self.process_subscription_status_event(event, session)
            case blpapi.Event.ADMIN               : self.process_admin_event(event, session)
            case _: pass


    def process_session_status_event(self, event: blpapi.Event, session: blpapi.Session):
        for msg in event:
            match msg.messageType():
                case SessionMsg.SESSION_STARTED         : logging.info(f"{self._log_prefix} Session started...")
                case SessionMsg.SESSION_STARTUP_FAILURE : logging.error(f"{self._log_prefix} Session startup failed")
                case SessionMsg.SESSION_CONNECTION_UP   : logging.info(f"{self._log_prefix} Session connection is up")
                case SessionMsg.SESSION_CONNECTION_DOWN : logging.info(f"{self._log_prefix} Session connection is down")
                case SessionMsg.SESSION_TERMINATED      : logging.info(f"{self._log_prefix} Session terminated")
                case _: logging.info(f"{self._log_prefix} {msg}")


    def process_service_status_event(self, event: blpapi.Event, session: blpapi.Session):
        for msg in event:
            match msg.messageType():
                case SessionMsg.SERVICE_OPENED       : logging.info(f"{self._log_prefix} Service opened...")
                case SessionMsg.SERVICE_OPEN_FAILURE : logging.error(f"{self._log_prefix} Service failed to open")
                case _: logging.info(f"{self._log_prefix} {msg}")


    def process_subscription_status_event(self, event: blpapi.Event, session: blpapi.Session):
        for msg in event:
            match msg.messageType():
                case SessionMsg.SUBSCRIPTION_STARTED    : logging.info(f"{self._log_prefix} Subscription started...")
                case SessionMsg.SUBSCRIPTION_FAILURE    : logging.error(f"{self._log_prefix} Subscription failed to start: {msg}")
                case SessionMsg.SUBSCRIPTION_TERMINATED : logging.error(f"{self._log_prefix} Subscription terminated")
                case _: logging.info(f"{self._log_prefix} {msg}")


    def process_admin_event(self, event: blpapi.Event, session: blpapi.Session):
        for msg in event:
            match msg.messageType():
                case SessionMsg.SLOW_CONSUMER_WARNING         : logging.warning(f"{self._log_prefix} SLOW CONSUMER WARNING")
                case SessionMsg.SLOW_CONSUMER_WARNING_CLEARED : logging.info(f"{self._log_prefix} SLOW CONSUMER WARNING cleared")
                case _: logging.info(f"{self._log_prefix} {msg}")