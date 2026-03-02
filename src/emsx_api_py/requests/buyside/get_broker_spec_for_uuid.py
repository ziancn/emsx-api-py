"""
Wrapper method to create 'GetBrokerSpecForUuid' request.
"""

import blpapi

from ..request_service_map import request_service_map


# blpapi names
# EMSX_TRADER_UUID = blpapi.Name("EMSX_TRADER_UUID")


def get_broker_spec_for_uuid(
        service: blpapi.Service,
        trader_uuid: int
) -> blpapi.Request:

    if service.name() not in request_service_map["GetBrokerSpecForUuid"]:
        raise ValueError(f"Invalid service received. Service name: {service.name()}")

    request = service.createRequest("GetBrokerSpecForUuid")

    request.set("uuid", trader_uuid)


    return request