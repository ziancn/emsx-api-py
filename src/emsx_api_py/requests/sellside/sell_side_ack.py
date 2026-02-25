"""
Wrapper method to create 'SellSideAck' request.
"""

import blpapi

from emsx_api_py.requests.request_service_map import request_service_map


# blpapi names
EMSX_REQUEST_SEQ = blpapi.Name("EMSX_REQUEST_SEQ")
EMSX_SEQUENCE    = blpapi.Name("EMSX_SEQUENCE")
EMSX_TRADER_UUID = blpapi.Name("EMSX_TRADER_UUID")


def sell_side_ack(
        service: blpapi.Service,
        emsx_request_seq: int | None,
        trader_uuid: int | None,
        emsx_sequence: int,
) -> blpapi.Request:

    if service.name() not in request_service_map["SellSideAck"]:
        raise ValueError(f"Invalid service received. Service name: {service.name()}")

    request = service.createRequest("SellSideAck")

    if emsx_request_seq: request.set(EMSX_REQUEST_SEQ, emsx_request_seq)
    if trader_uuid: request.set(EMSX_TRADER_UUID, trader_uuid)

    request.append(EMSX_SEQUENCE, emsx_sequence)


    return request