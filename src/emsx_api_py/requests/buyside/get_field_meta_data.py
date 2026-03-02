"""
Wrapper method to create 'GetFieldMetaData' request.
"""

import blpapi

from typing import List

from ..request_service_map import request_service_map

# blpapi names
EMSX_REQUEST_SEQ = blpapi.Name("EMSX_REQUEST_SEQ")
EMSX_FIELD_NAMES = blpapi.Name("EMSX_FIELD_NAMES")


def get_field_meta_data(
        service: blpapi.Service,
        fields: List[str],
        emsx_request_seq: str | None = None
) -> blpapi.Request:
    """
    """

    if service.name() not in request_service_map["GetFieldMetaData"]:
        raise ValueError(f"Invalid service received. Service name: {service.name()}")

    request = service.createRequest("GetFieldMetaData")

    if emsx_request_seq is not None: request.set(EMSX_REQUEST_SEQ, emsx_request_seq)

    for field in fields:
        request.getElement(EMSX_FIELD_NAMES).appendValue(field)


    return request