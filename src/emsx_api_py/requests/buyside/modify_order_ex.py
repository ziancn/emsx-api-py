"""
Wrapper method to create 'ModifyOrderEx' request.
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
EMSX_TICKER     = blpapi.Name("EMSX_TICKER")
# Optional parameters
EMSX_HAND_INSTRUCTION = blpapi.Name("EMSX_HAND_INSTRUCTION")
EMSX_ACCOUNT          = blpapi.Name("EMSX_ACCOUNT")
EMSX_CFD_FLAG         = blpapi.Name("EMSX_CFD_FLAG")
EMSX_EXEC_INSTRUCTION = blpapi.Name("EMSX_EXEC_INSTRUCTION")
EMSX_GET_WARNINGS     = blpapi.Name("EMSX_GET_WARNINGS")
EMSX_GTD_DATE         = blpapi.Name("EMSX_GTD_DATE")
EMSX_INVESTOR_ID      = blpapi.Name("EMSX_INVESTOR_ID")
EMSX_LIMIT_PRICE      = blpapi.Name("EMSX_LIMIT_PRICE")
EMSX_NOTES            = blpapi.Name("EMSX_NOTES")
EMSX_REQUEST_SEQ      = blpapi.Name("EMSX_REQUEST_SEQ")
EMSX_STOP_PRICE       = blpapi.Name("EMSX_STOP_PRICE")


class ModifyOrderExOptional(TypedDict, total=False):
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



def modify_order_ex(
        service: blpapi.Service,
        *,
        emsx_sequence: int,
        emsx_amount: int,
        emsx_ticker: str,
        emsx_order_type: str,
        emsx_tif: str = "DAY",
        # Optional parameters
        **kwargs: Unpack[ModifyOrderExOptional]
) -> blpapi.Request:

    if service.name() not in request_service_map["ModifyOrderEx"]:
        raise ValueError(f"Invalid service received. Service name: {service.name()}")

    request = service.createRequest("ModifyOrderEx")

    # Mandatory parameters
    mandatory_params = {
        EMSX_SEQUENCE: emsx_sequence,
        EMSX_AMOUNT: emsx_amount,
        EMSX_TICKER: emsx_ticker,
        EMSX_ORDER_TYPE: emsx_order_type,
        EMSX_TIF: emsx_tif
    }

    for field, value in mandatory_params.items():
        request.set(field, value)


    # Optional params
    emsx_name_map = {
        "emsx_hand_instruction" : EMSX_HAND_INSTRUCTION,
        "emsx_account"          : EMSX_ACCOUNT,
        "emsx_cfd_flag"         : EMSX_CFD_FLAG,
        "emsx_exec_instruction" : EMSX_EXEC_INSTRUCTION,
        "emsx_get_warnings"     : EMSX_GET_WARNINGS,
        "emsx_gtd_date"         : EMSX_GTD_DATE,
        "emsx_investor_id"      : EMSX_INVESTOR_ID,
        "emsx_limit_price"      : EMSX_LIMIT_PRICE,
        "emsx_notes"            : EMSX_NOTES,
        "emsx_request_seq"      : EMSX_REQUEST_SEQ,
        "emsx_stop_price"       : EMSX_STOP_PRICE
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

    # If modifying on behalf of another trader, set the order owner's UUID
    # request.set("EMSX_TRADER_UUID", 1234567)

    return request