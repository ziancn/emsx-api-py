"""
Wrapper method to create 'CancelRoute' request.
"""

import blpapi

from typing import Tuple

from ..request_service_map import request_service_map


# blpapi names
EMSX_REQUEST_SEQ = blpapi.Name("EMSX_REQUEST_SEQ")
EMSX_TRADER_UUID = blpapi.Name("EMSX_TRADER_UUID")
ROUTES           = blpapi.Name("ROUTES")
EMSX_SEQUENCE    = blpapi.Name("EMSX_SEQUENCE")
EMSX_ROUTE_ID    = blpapi.Name("EMSX_ROUTE_ID")


def cancel_route(
        service: blpapi.Service,
        emsx_request_seq: int | None,
        trader_uuid: int | None,
        routes: Tuple[int, int]       # (emsx_sequence, route_id), i.e. (1234567, 1)
) -> blpapi.Request:

    if service.name() not in request_service_map["CancelRoute"]:
        raise ValueError(f"Invalid service received. Service name: {service.name()}")

    request = service.createRequest("CancelRoute")

    if emsx_request_seq: request.set(EMSX_REQUEST_SEQ, emsx_request_seq)
    if trader_uuid: request.set(EMSX_TRADER_UUID, trader_uuid)

    # Append routes to cancel:
    for emsx_sequence, route_id in routes:
        # Append a new route to cancel
        route_to_cancel = request.getElement(ROUTES).appendElement()
        # Specify which route of which sequence to cancel
        route_to_cancel.getElement(EMSX_SEQUENCE).setValue(emsx_sequence)
        route_to_cancel.getElement(EMSX_ROUTE_ID).setValue(route_id)


    return request