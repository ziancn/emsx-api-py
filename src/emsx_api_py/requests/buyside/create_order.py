"""
Wrapper method to create 'CreateOrder' request.
"""

import blpapi
import logging

from dataclasses import dataclass, asdict

from ..request_service_map import request_service_map


# blpapi names
# Mandatory parameters
EMSX_TICKER           = blpapi.Name("EMSX_TICKER")
EMSX_AMOUNT           = blpapi.Name("EMSX_AMOUNT")
EMSX_ORDER_TYPE       = blpapi.Name("EMSX_ORDER_TYPE")
EMSX_TIF              = blpapi.Name("EMSX_TIF")
EMSX_HAND_INSTRUCTION = blpapi.Name("EMSX_HAND_INSTRUCTION")
EMSX_SIDE             = blpapi.Name("EMSX_SIDE")
# Optional parameters
EMSX_ACCOUNT              = blpapi.Name("EMSX_ACCOUNT")
EMSX_BOOKNAME             = blpapi.Name("EMSX_BOOKNAME")
EMSX_BROKER               = blpapi.Name("EMSX_BROKER")
EMSX_CFD_FLAG             = blpapi.Name("EMSX_CFD_FLAG")
EMSX_CLEARING_ACCOUNT     = blpapi.Name("EMSX_CLEARING_ACCOUNT")
EMSX_CLEARING_FIRM        = blpapi.Name("EMSX_CLEARING_FIRM")
EMSX_CUSTOM_NOTE1         = blpapi.Name("EMSX_CUSTOM_NOTE1")
EMSX_CUSTOM_NOTE2         = blpapi.Name("EMSX_CUSTOM_NOTE2")
EMSX_CUSTOM_NOTE3         = blpapi.Name("EMSX_CUSTOM_NOTE3")
EMSX_CUSTOM_NOTE4         = blpapi.Name("EMSX_CUSTOM_NOTE4")
EMSX_CUSTOM_NOTE5         = blpapi.Name("EMSX_CUSTOM_NOTE5")
EMSX_EXCHANGE_DESTINATION = blpapi.Name("EMSX_EXCHANGE_DESTINATION")
EMSX_EXEC_INSTRUCTION     = blpapi.Name("EMSX_EXEC_INSTRUCTION")
EMSX_GET_WARNINGS         = blpapi.Name("EMSX_GET_WARNINGS")
EMSX_GTD_DATE             = blpapi.Name("EMSX_GTD_DATE")
EMSX_LIMIT_PRICE          = blpapi.Name("EMSX_LIMIT_PRICE")
EMSX_LOCATE_BROKER        = blpapi.Name("EMSX_LOCATE_BROKER")
EMSX_LOCATE_ID            = blpapi.Name("EMSX_LOCATE_ID")
EMSX_LOCATE_REQ           = blpapi.Name("EMSX_LOCATE_REQ")
EMSX_NOTES                = blpapi.Name("EMSX_NOTES")
EMSX_ODD_LOT              = blpapi.Name("EMSX_ODD_LOT")
EMSX_ORDER_ORIGIN         = blpapi.Name("EMSX_ORDER_ORIGIN")
EMSX_ROUTE_REF_ID         = blpapi.Name("EMSX_ROUTE_REF_ID")
EMSX_P_A                  = blpapi.Name("EMSX_P_A")
EMSX_RELEASE_TIME         = blpapi.Name("EMSX_RELEASE_TIME")
EMSX_REQUEST_SEQ          = blpapi.Name("EMSX_REQUEST_SEQ")
EMSX_SETTLE_CURRENCY      = blpapi.Name("EMSX_SETTLE_CURRENCY")
EMSX_SETTLE_DATE          = blpapi.Name("EMSX_SETTLE_DATE")
EMSX_SETTLE_TYPE          = blpapi.Name("EMSX_SETTLE_TYPE")
EMSX_STOP_PRICE           = blpapi.Name("EMSX_STOP_PRICE")


# Optional parameters
@dataclass
class CreateOrderOptionalParams:
    emsx_account             : str | None = None        # "TestAccount"
    emsx_bookname            : str | None = None        # "BookName"
    emsx_broker              : str | None = None        # "CLSA"
    emsx_cfd_flag            : bool | None = None       # "0" or "1"
    emsx_clearing_account    : str | None = None        # "ClrAccName"
    emsx_clearing_firm       : str | None = None        # "FirmName"
    emsx_custom_note1        : str | None = None
    emsx_custom_note2        : str | None = None
    emsx_custom_note3        : str | None = None
    emsx_custom_note4        : str | None = None
    emsx_custom_note5        : str | None = None
    emsx_exchange_destination: str | None = None        # "XSHG"
    emsx_exec_instruction    : str | None = None        # "AnyInst"
    emsx_get_warnings        : bool | None = None       # "0" or "1"
    emsx_gtd_date            : str | None = None        # "yyyymmdd"
    emsx_limit_price         : float | None = None      # 123.45
    emsx_locate_broker       : str | None = None        # "CLSA"
    emsx_locate_id           : int | None = None        # "SomeID"
    emsx_locate_req          : bool | None = None       # "Y"
    emsx_notes               : str | None = None        # "Some notes about the order"
    emsx_odd_lot             : bool | None = None       # "0" or "1"
    emsx_order_origin        : str | None = None        # ""
    emsx_route_ref_id        : str | None = None        # "SomeID"
    emsx_p_a                 : bool | None = None       # "0" or "1"
    emsx_release_time        : str | None = None        # "yyyymmdd-HH:MM:SS"
    emsx_request_seq         : int | None = None        # 12345
    emsx_settle_currency     : str | None = None        # "USD"
    emsx_settle_date         : int | None = None        # 20260226
    emsx_settle_type         : str | None = None        # "T+2"
    emsx_stop_price          : float | None = None      # 123.45


def create_order(
        service: blpapi.Service,
        emsx_ticker: str,
        emsx_amount: int,
        emsx_order_type: str,  # MKT, LMT, etc.
        emsx_side: str,        # BUY, SELL, SHRT, COVR, B/O, B/C, S/O, S/C
        emsx_tif: str = "DAY",
        emsx_hand_instruction: str = "ANY",
        # Optional parameters
        optional_params: CreateOrderOptionalParams = CreateOrderOptionalParams()
) -> blpapi.Request:

    if service.name() not in request_service_map["CreateOrder"]:
        raise ValueError(f"Invalid service received. Service name: {service.name()}")

    request = service.createRequest("CreateOrder")


    # Mandatory parameters
    mandatory_params = {
        EMSX_TICKER: emsx_ticker,
        EMSX_AMOUNT: emsx_amount,
        EMSX_ORDER_TYPE: emsx_order_type,
        EMSX_SIDE: emsx_side,
        EMSX_TIF: emsx_tif,
        EMSX_HAND_INSTRUCTION: emsx_hand_instruction
    }

    for field, value in mandatory_params.items():
        request.set(field, value)


    # Optional params
    optional_params = asdict(optional_params)
    optional_mapping = {
        "emsx_account"             : EMSX_ACCOUNT,
        "emsx_bookname"            : EMSX_BOOKNAME,
        "emsx_broker"              : EMSX_BROKER,
        "emsx_cfd_flag"            : EMSX_CFD_FLAG,
        "emsx_clearing_account"    : EMSX_CLEARING_ACCOUNT,
        "emsx_clearing_firm"       : EMSX_CLEARING_FIRM,
        "emsx_custom_note1"        : EMSX_CUSTOM_NOTE1,
        "emsx_custom_note2"        : EMSX_CUSTOM_NOTE2,
        "emsx_custom_note3"        : EMSX_CUSTOM_NOTE3,
        "emsx_custom_note4"        : EMSX_CUSTOM_NOTE4,
        "emsx_custom_note5"        : EMSX_CUSTOM_NOTE5,
        "emsx_exchange_destination": EMSX_EXCHANGE_DESTINATION,
        "emsx_exec_instruction"    : EMSX_EXEC_INSTRUCTION,
        "emsx_get_warnings"        : EMSX_GET_WARNINGS,
        "emsx_gtd_date"            : EMSX_GTD_DATE,
        "emsx_limit_price"         : EMSX_LIMIT_PRICE,
        "emsx_locate_broker"       : EMSX_LOCATE_BROKER,
        "emsx_locate_id"           : EMSX_LOCATE_ID,
        "emsx_locate_req"          : EMSX_LOCATE_REQ,
        "emsx_notes"               : EMSX_NOTES,
        "emsx_odd_lot"             : EMSX_ODD_LOT,
        "emsx_order_origin"        : EMSX_ORDER_ORIGIN,
        "emsx_route_ref_id"        : EMSX_ROUTE_REF_ID,
        "emsx_p_a"                 : EMSX_P_A,
        "emsx_release_time"        : EMSX_RELEASE_TIME,
        "emsx_request_seq"         : EMSX_REQUEST_SEQ,
        "emsx_settle_currency"     : EMSX_SETTLE_CURRENCY,
        "emsx_settle_date"         : EMSX_SETTLE_DATE,
        "emsx_settle_type"         : EMSX_SETTLE_TYPE,
        "emsx_stop_price"          : EMSX_STOP_PRICE,
    }

    for param_name, value in optional_params.items():
        if value is None:
            continue

        if optional_mapping.get(param_name) is None:
            logging.warning(f"Unexpected parameter '{param_name}' provided. No corresponding RouteEx field found. Skipping this parameter.")
            continue

        request.set(optional_mapping[param_name], value)


    return request