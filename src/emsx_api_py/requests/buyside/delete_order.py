"""
Wrapper method to create 'DeleteOrder' request.
"""

import blpapi

from typing import List

from ..request_service_map import request_service_map

# blpapi names
EMSX_REQUEST_SEQ = blpapi.Name("EMSX_REQUEST_SEQ")
EMSX_SEQUENCE    = blpapi.Name("EMSX_SEQUENCE")


def delete_order(
        service: blpapi.Service,
        emsx_request_seq: str | None,
        emsx_sequences: List[int]
) -> blpapi.Request:
    """
    """

    if service.name() not in request_service_map["DeleteOrder"]:
        raise ValueError(f"Invalid service received. Service name: {service.name()}")

    request = service.createRequest("DeleteOrder")

    if emsx_request_seq: request.set(EMSX_REQUEST_SEQ, emsx_request_seq)

    for seq in emsx_sequences:
        request.getElement(EMSX_SEQUENCE).appendValue(seq)


    return request