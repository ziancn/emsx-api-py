"""
EMSX modules protocol template
"""

import blpapi

from typing import Protocol, TYPE_CHECKING


if TYPE_CHECKING:
    from ..session_manager import SessionManager


class ModuleProtocol(Protocol):
    def handle_event(
            self,
            etype  : int,
            event  : blpapi.Event,
            session: blpapi.Session,
            manager: "SessionManager",
    ):
        ...