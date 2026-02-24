"""
Wrapper method to create 'AssignTrader' request.
"""

import blpapi

from typing import List

from .request_service_map import request_service_map

# blpapi names
EMSX_SEQUENCE             = blpapi.Name("EMSX_SEQUENCE")
EMSX_ASSIGNEE_TRADER_UUID = blpapi.Name("EMSX_ASSIGNEE_TRADER_UUID")


def assign_trader(
        service: blpapi.Service,
        emsx_sequence: int | List[int],
        trader_uuid: int
) -> blpapi.Request:

    if service.name() not in request_service_map["AssignTrader"]:
        raise ValueError(f"Invalid service received. Service name: {service.name()}")

    request = service.createRequest("AssignTrader")

    if isinstance(emsx_sequence, int):
        request.append(EMSX_SEQUENCE, emsx_sequence)
    elif isinstance(emsx_sequence, list):
        for seq in emsx_sequence:
            request.append(EMSX_SEQUENCE, seq)
    else:
        raise ValueError(f"Invalid type for emsx_sequence. Expected int or List[int], got {type(emsx_sequence)}")

    request.set(EMSX_ASSIGNEE_TRADER_UUID, trader_uuid)


    return request