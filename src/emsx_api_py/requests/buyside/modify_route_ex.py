"""
Wrapper method to create 'ModifyRouteEx' request.
"""

import blpapi
import logging

from typing import TypedDict, Unpack, NotRequired

from ..request_service_map import request_service_map


# blpapi names
# Mandatory parameters
EMSX_SEQUENCE   = blpapi.Name("EMSX_SEQUENCE")
EMSX_AMOUNT     = blpapi.Name("EMSX_AMOUNT")
EMSX_ORDER_TYPE = blpapi.Name("EMSX_ORDER_TYPE")
EMSX_TIF        = blpapi.Name("EMSX_TIF")
EMSX_ROUTE_ID   = blpapi.Name("EMSX_ROUTE_ID")
# Optional parameters
EMSX_ACCOUNT              = blpapi.Name("EMSX_ACCOUNT")
EMSX_CLEARING_ACCOUNT     = blpapi.Name("EMSX_CLEARING_ACCOUNT")
EMSX_CLEARING_FIRM        = blpapi.Name("EMSX_CLEARING_FIRM")
EMSX_COMM_TYPE            = blpapi.Name("EMSX_COMM_TYPE")
EMSX_EXCHANGE_DESTINATION = blpapi.Name("EMSX_EXCHANGE_DESTINATION")
EMSX_GET_WARNINGS         = blpapi.Name("EMSX_GET_WARNINGS")
EMSX_GTD_DATE             = blpapi.Name("EMSX_GTD_DATE")
EMSX_LIMIT_PRICE          = blpapi.Name("EMSX_LIMIT_PRICE")
EMSX_LOC_BROKER           = blpapi.Name("EMSX_LOC_BROKER")
EMSX_LOC_ID               = blpapi.Name("EMSX_LOC_ID")
EMSX_LOC_REQ              = blpapi.Name("EMSX_LOC_REQ")
EMSX_NOTES                = blpapi.Name("EMSX_NOTES")
EMSX_ODD_LOT              = blpapi.Name("EMSX_ODD_LOT")
EMSX_P_A                  = blpapi.Name("EMSX_P_A")
EMSX_REQUEST_SEQ          = blpapi.Name("EMSX_REQUEST_SEQ")
EMSX_STOP_PRICE           = blpapi.Name("EMSX_STOP_PRICE")
EMSX_TRADER_NOTES         = blpapi.Name("EMSX_TRADER_NOTES")
EMSX_USER_COMM_RATE       = blpapi.Name("EMSX_USER_COMM_RATE")
EMSX_USER_FEES            = blpapi.Name("EMSX_USER_FEES")


class ModifyRouteExOptional(TypedDict, total=False):
    emsx_hand_instruction     : NotRequired[str]
    emsx_account              : NotRequired[str]
    emsx_cfd_flag             : NotRequired[str]
    emsx_exec_instruction     : NotRequired[str]
    emsx_get_warnings         : NotRequired[str]
    emsx_gtd_date             : NotRequired[str]
    emsx_investor_id          : NotRequired[str]
    emsx_limit_price          : NotRequired[float]
    emsx_notes                : NotRequired[str]
    emsx_request_seq          : NotRequired[int]
    emsx_stop_price           : NotRequired[float]


def modify_route_ex(
        service: blpapi.Service,
        *,
        emsx_sequence: int,
        emsx_route_id: int,
        emsx_amount: int,
        emsx_order_type: str,
        emsx_tif: str = "DAY",
        # Optional parameters
        **kwargs: Unpack[ModifyRouteExOptional]
) -> blpapi.Request:

    if service.name() not in request_service_map["ModifyOrderEx"]:
        raise ValueError(f"Invalid service received. Service name: {service.name()}")

    request = service.createRequest("ModifyOrderEx")

    # Mandatory parameters
    mandatory_params = {
        EMSX_SEQUENCE: emsx_sequence,
        EMSX_ROUTE_ID: emsx_route_id,
        EMSX_AMOUNT: emsx_amount,
        EMSX_ORDER_TYPE: emsx_order_type,
        EMSX_TIF: emsx_tif
    }

    for field, value in mandatory_params.items():
        request.set(field, value)


    # Optional params
    emsx_name_map = {
        "emsx_account"              : EMSX_ACCOUNT,
        "emsx_clearing_account"     : EMSX_CLEARING_ACCOUNT,
        "emsx_clearing_firm"        : EMSX_CLEARING_FIRM,
        "emsx_comm_type"            : EMSX_COMM_TYPE,
        "emsx_exchange_destination" : EMSX_EXCHANGE_DESTINATION,
        "emsx_get_warnings"         : EMSX_GET_WARNINGS,
        "emsx_gtd_date"             : EMSX_GTD_DATE,
        "emsx_limit_price"          : EMSX_LIMIT_PRICE,
        "emsx_loc_broker"           : EMSX_LOC_BROKER,
        "emsx_loc_id"               : EMSX_LOC_ID,
        "emsx_loc_req"              : EMSX_LOC_REQ,
        "emsx_notes"                : EMSX_NOTES,
        "emsx_odd_lot"              : EMSX_ODD_LOT,
        "emsx_p_a"                  : EMSX_P_A,
        "emsx_request_seq"          : EMSX_REQUEST_SEQ,
        "emsx_stop_price"           : EMSX_STOP_PRICE,
        "emsx_trader_notes"         : EMSX_TRADER_NOTES,
        "emsx_user_comm_rate"       : EMSX_USER_COMM_RATE,
        "emsx_user_fees"            : EMSX_USER_FEES
    }

    for param_name, value in kwargs.items():
        if value is None:
            continue

        if emsx_name_map.get(param_name) is None:
            logging.warning(f"Unexpected parameter '{param_name}' provided. Skipping this parameter.")
            continue

        request.set(emsx_name_map[param_name], value)

    # Note: When changing order type to a LMT order, you will need to provide the EMSX_LIMIT_PRICE value.
    #       When changing order type away from LMT order, you will need to reset the EMSX_LIMIT_PRICE value
    #       by setting the content to -99999

    # Note: To clear down the stop price, set the content to -1

    return request

