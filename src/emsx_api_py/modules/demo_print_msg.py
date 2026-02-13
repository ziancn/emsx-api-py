"""
This is a demo module that prints the msg of any event received.
"""
import blpapi

from .protocol import ModuleProtocol

class DemoPrintMsg(ModuleProtocol):

    def __init__(self, name: str = "DemoPrintMsg"):
        self._name = name

    def handle_event(
            self,
            etype  : int,
            event  : blpapi.Event,
            session: blpapi.Session,
            manager: "SessionManager",
    ):
        for msg in event:
            print(f"[{self._name}] Event Type: {etype}, Msg: {msg}")