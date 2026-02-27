"""
Wrapper method to create 'GetTeams' request.
"""

import blpapi

from ..request_service_map import request_service_map

# blpapi names
EMSX_REQUEST_SEQ = blpapi.Name("EMSX_REQUEST_SEQ")


def get_teams(
        service: blpapi.Service,
        emsx_request_seq: str | None,
) -> blpapi.Request:
    """
    """

    if service.name() not in request_service_map["GetTeams"]:
        raise ValueError(f"Invalid service received. Service name: {service.name()}")

    request = service.createRequest("GetTeams")

    if emsx_request_seq: request.set(EMSX_REQUEST_SEQ, emsx_request_seq)


    return request