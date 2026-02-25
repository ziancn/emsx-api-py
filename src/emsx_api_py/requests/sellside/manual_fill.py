"""
Wrapper method to create 'ManualFill' request.
"""

import blpapi

from emsx_api_py.requests.request_service_map import request_service_map


# blpapi names
EMSX_REQUEST_SEQ      = blpapi.Name("EMSX_REQUEST_SEQ")
EMSX_SEQUENCE         = blpapi.Name("EMSX_SEQUENCE")
EMSX_TRADER_UUID      = blpapi.Name("EMSX_TRADER_UUID")
ROUTE_TO_FILL         = blpapi.Name("ROUTE_TO_FILL")
EMSX_ROUTE_ID         = blpapi.Name("EMSX_ROUTE_ID")
FILLS                 = blpapi.Name("FILLS")
EMSX_FILL_AMOUNT      = blpapi.Name("EMSX_FILL_AMOUNT")
EMSX_FILL_PRICE       = blpapi.Name("EMSX_FILL_PRICE")
EMSX_FILL_DATE_TIME   = blpapi.Name("EMSX_FILL_DATE_TIME")
LEGACY                = blpapi.Name("Legacy")
EMSX_FILL_DATE        = blpapi.Name("EMSX_FILL_DATE")
EMSX_FILL_TIME        = blpapi.Name("EMSX_FILL_TIME")
EMSX_FILL_TIME_FORMAT = blpapi.Name("EMSX_FILL_TIME_FORMAT")


def manual_fill(
        service: blpapi.Service,
        emsx_request_seq: int | None,
        trader_uuid: int | None,
        emsx_sequence: int,
        route_id: int,
        fill_amount: int,
        fill_price: float,
        # Only use "Legacy" format here for simplicity.
        fill_date: int,
        fill_seconds: int,
) -> blpapi.Request:

    if service.name() not in request_service_map["ManualFill"]:
        raise ValueError(f"Invalid service received. Service name: {service.name()}")

    request = service.createRequest("ManualFill")

    if emsx_request_seq: request.set(EMSX_REQUEST_SEQ, emsx_request_seq)
    if trader_uuid: request.set(EMSX_TRADER_UUID, trader_uuid)

    route_to_fill = request.getElement(ROUTE_TO_FILL)
    route_to_fill.setElement(EMSX_SEQUENCE, emsx_sequence)
    route_to_fill.setElement(EMSX_ROUTE_ID, route_id)

    new_fill = request.getElement(FILLS).appendElement()
    new_fill.setElement(EMSX_FILL_AMOUNT, fill_amount)
    new_fill.setElement(EMSX_FILL_PRICE, fill_price)

    new_fill_dt = new_fill.getElement(EMSX_FILL_DATE_TIME)

    legacy = new_fill_dt.setChoice(LEGACY)
    legacy.setElement(EMSX_FILL_DATE, fill_date)
    legacy.setElement(EMSX_FILL_TIME, fill_seconds)
    legacy.setElement(EMSX_FILL_TIME_FORMAT, "SecondsFromMidnight")


    return request