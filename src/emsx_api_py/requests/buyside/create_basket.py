"""
Wrapper method to create 'CreateBasket' request.
"""

import blpapi

from typing import List

from ..request_service_map import request_service_map


# blpapi names
EMSX_BASKET_NAME = blpapi.Name("EMSX_BASKET_NAME")
EMSX_SEQUENCE    = blpapi.Name("EMSX_SEQUENCE")


def create_basket(
        service: blpapi.Service,
        basket_name: str,
        sequences: List[int]
) -> blpapi.Request:

    if service.name() not in request_service_map["CreateBasket"]:
        raise ValueError(f"Invalid service received. Service name: {service.name()}")

    request = service.createRequest("CreateBasket")

    # Set basket name
    request.set(EMSX_BASKET_NAME, basket_name)

    # Add any numbers of orders
    for seq in sequences:
        request.append(EMSX_SEQUENCE, seq)


    return request