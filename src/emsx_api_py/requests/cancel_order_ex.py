"""
Wrapper method to create 'CancelOrderEx' request.
"""

import blpapi

from .request_service_map import request_service_map


# blpapi names
EMSX_TRADER_UUID = blpapi.Name("EMSX_TRADER_UUID")
EMSX_SEQUENCE    = blpapi.Name("EMSX_SEQUENCE")
EMSX_REQUEST_SEQ = blpapi.Name("EMSX_REQUEST_SEQ")


def cancel_order_ex(
        service: blpapi.Service,
        emsx_sequence: int | list[int] | None,
        trader_uuid: int | None,
        emsx_request_seq: int | None = None
) -> blpapi.Request:

    if service.name() not in request_service_map["CancelOrderEx"]:
        raise ValueError(f"Invalid service received. Service name: {service.name()}")

    request = service.createRequest("CancelOrderEx")

    # Filter on trader uuid
    if trader_uuid: request.set(EMSX_TRADER_UUID, trader_uuid)
    if emsx_request_seq: request.set(EMSX_REQUEST_SEQ, emsx_request_seq)

    # Filter on sequence number(s)
    if emsx_sequence:
        if isinstance(emsx_sequence, int):
            request.getElement(EMSX_SEQUENCE).appendValue(emsx_sequence)
        elif isinstance(emsx_sequence, list):
            for seq in emsx_sequence:
                request.getElement(EMSX_SEQUENCE).appendValue(seq)
        else:
            raise ValueError(f"Invalid type for emsx_sequence. Expected int or List[int], got {type(emsx_sequence)}")


    return request