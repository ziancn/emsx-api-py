"""
This module houses the SessionManager class, which controls session lifecycle and event handling.
"""

import blpapi
import logging

from typing import List, Callable, Dict

from .modules.protocol import ModuleProtocol


# Typehint
ResponseHandler = Callable[[blpapi.Message, blpapi.Session], None]


class SessionManager:
    """
    SessionManager controls and session connection, request/response and event distribution
    to registered modules which you can customize and extend.
    """
    def __init__(self, host: str = "localhost", port: int = 8194):
        session_options = blpapi.SessionOptions()
        session_options.setServerHost(host)
        session_options.setServerPort(port)

        self._session = blpapi.Session(session_options, self._process_event)
        self._response_handlers: Dict[blpapi.CorrelationId, ResponseHandler] = {}
        self._modules: List[ModuleProtocol] = []


    # PRIVATE
    def _process_event(self, event: blpapi.Event, session: blpapi.Session):
        logging.info(f"[SessionManager] EVENT received: {event.eventType()}")

        # 1. Dispatch responses
        if event.eventType() in (blpapi.Event.RESPONSE, blpapi.Event.PARTIAL_RESPONSE):
            self._dispatch_response(event, session)

        # 2. Broadcast to all registered modules
        for module in self._modules:
            try:
               module.process_event(event, session)
            except Exception as e:
               logging.exception(f"[SessionManager] Module '{module}' error: {e}")


    def _dispatch_response(self, event: blpapi.Event, session: blpapi.Session):
        for msg in event:
            if not msg.correlationIds(): continue
            
            cid_value = msg.correlationIds()[0].value()
            handler = self._response_handlers.get(cid_value)
            
            if handler is None: continue
            
            try:
                handler(msg, session)
            except Exception as exc:
                logging.exception(f"[SessionManager] Response handler error: {exc}")


    # PUBLIC
    @property
    def session(self) -> blpapi.Session:
        return self._session


    def start(self):
        if not self._session.start():
            raise RuntimeError("Failed to start EMSX session")


    def start_async(self):
        if not self._session.startAsync():
            raise RuntimeError("Failed to start(async) EMSX session")


    def stop(self):
        self._session.stop()


    def register_module(self, module: ModuleProtocol):
        if module not in self._modules:
            self._modules.append(module)


    def send_request(
           self,
           request: blpapi.Request,
           handler: ResponseHandler
    ) -> blpapi.CorrelationId:
        cid = blpapi.CorrelationId()
        self._response_handlers[cid.value()] = handler
        self._session.sendRequest(request, correlationId=cid)
        return cid