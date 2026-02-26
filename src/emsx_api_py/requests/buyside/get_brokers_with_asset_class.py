"""
Wrapper method to create 'GetBrokersWithAssetClass' request.
"""

import blpapi

from ..request_service_map import request_service_map


# blpapi names
EMSX_REQUEST_SEQ = blpapi.Name("EMSX_REQUEST_SEQ")
EMSX_ASSET_CLASS = blpapi.Name("EMSX_ASSET_CLASS")
EMSX_BROKER      = blpapi.Name("EMSX_BROKER")
EMSX_STRATEGY    = blpapi.Name("EMSX_STRATEGY")


def get_brokers_with_asset_class(
        service: blpapi.Service,
        emsx_request_seq: str | None,
        asset_class: str,
) -> blpapi.Request:
    """
    """

    if service.name() not in request_service_map["GetBrokersWithAssetClass"]:
        raise ValueError(f"Invalid service received. Service name: {service.name()}")

    request = service.createRequest("GetBrokersWithAssetClass")

    if emsx_request_seq: request.set(EMSX_REQUEST_SEQ, emsx_request_seq)

    # Set asset class
    request.set(EMSX_ASSET_CLASS, asset_class)
    

    return request