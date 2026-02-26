"""
This module monitors general status like
session status, services status, subscription status and subscription heartbeat.
"""

import blpapi
import logging

from .protocol import ModuleProtocol


class StatusMonitor(ModuleProtocol):
    def process_event(
            self,
            event  : blpapi.Event,
            session: blpapi.Session,
    ):
        et = event.eventType()
        if   et == blpapi.Event.SESSION_STATUS     : self.process_session_status_event(event, session)
        elif et == blpapi.Event.SERVICE_STATUS     : self.process_service_status_event(event, session)
        elif et == blpapi.Event.SUBSCRIPTION_STATUS: self.process_subscription_status_event(event, session)
        else: pass


    def process_session_status_event(self, event: blpapi.Event, session: blpapi.Session):
        for msg in event:
            if msg.messageType() == blpapi.Name("SessionStarted"):
                logging.info(f"[{self.__class__.__name__}] Session started...")
            elif msg.messageType() == blpapi.Name("SessionStartupFailure"):
                logging.error(f"[{self.__class__.__name__}] Session startup failed")
            else:
                logging.info(f"[{self.__class__.__name__}] {msg}")


    def process_service_status_event(self, event: blpapi.Event, session: blpapi.Session):
        for msg in event:
            if msg.messageType() == blpapi.Name("ServiceOpened"):
                logging.info(f"[{self.__class__.__name__}] Service opened...")
            elif msg.messageType() == blpapi.Name("ServiceOpenFailure"):
                logging.error(f"[{self.__class__.__name__}] Service failed to open")
            else:
                logging.info(f"[{self.__class__.__name__}] {msg}")


    def process_subscription_status_event(self, event: blpapi.Event, session: blpapi.Session):
        for msg in event:
            if msg.messageType() == blpapi.Name("SubscriptionStarted"):
                logging.info(f"[{self.__class__.__name__}] Subscription started...")
            elif msg.messageType() == blpapi.Name("SubscriptionFailure"):
                logging.error(f"[{self.__class__.__name__}] Subscription failed to start")
            elif msg.messageType() == blpapi.Name("SubscriptionTerminated"):
                logging.error(f"[{self.__class__.__name__}] Subscription terminated")
            else:
                logging.info(f"[{self.__class__.__name__}] {msg}")