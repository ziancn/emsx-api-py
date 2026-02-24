"""
Wrapper method to create 'GetFills' request.
"""

import blpapi

from typing import List

from .request_service_map import request_service_map


# blpapi names
FROM_DATETIME     = blpapi.Name("FromDateTime")
TO_DATETIME       = blpapi.Name("ToDateTime")
SCOPE             = blpapi.Name("Scope")
TEAM              = blpapi.Name("Team")
TRADING_SYSTEM    = blpapi.Name("TradingSystem")
UUIDS             = blpapi.Name("Uuids")
FILTER_BY         = blpapi.Name("FilterBy")
BASKET            = blpapi.Name("Basket")
MULTILEG          = blpapi.Name("Multileg")
ORDERS_AND_ROUTES = blpapi.Name("OrdersAndRoutes")
ORDER_ID          = blpapi.Name("OrderId")
ROUTE_ID          = blpapi.Name("RouteId")


def request_get_fills(
        service: blpapi.Service,
        start_dt: str,
        end_dt: str,
        scope_choice: str,
        # Scope/Filter parameters
        team_name: str | None,
        uuids: int | List[int] | None,
        filter_choice: str | None,
        basket_name: str | None,
        multileg_name: str | None,
        order_id: int | None,
        route_id: int | None,
) -> blpapi.Request:

    if service.name() not in request_service_map["GetFills"]:
        raise ValueError(f"Invalid service received. Service name: {service.name()}")

    request = service.createRequest("GetFills")
    request.set(FROM_DATETIME, start_dt)
    request.set(TO_DATETIME, end_dt)

    scope = request.getElement(SCOPE)


    # 1st level filtering: by Team, TradingSystem or Uuids
    if scope_choice.lower() == "team":
        scope.setChoice(TEAM)
        if team_name: scope.setElement(TEAM, team_name)
        else: raise ValueError("Missing parameter 'team_name'.")

    elif scope_choice.lower() == "uuids":
        scope.setChoice(UUIDS)
        if uuids:
            if isinstance(uuids, int): uuids = [uuids]
            for uuid in uuids:
                scope.getElement(UUIDS).appendValue(uuid)
        else:
            raise ValueError("Missing parameter 'uuids'.")

    elif scope_choice.lower() == "tradingsystem":
        # Note: Most of the time you will never use TradingSystem to filter.
        scope.setChoice(TRADING_SYSTEM)
        # If you encounter case where you really have different trading systems,
        # you need to pass the name of system to setElement. `True` is a mechanism
        # that tells server to link this UUID's current trading system.
        scope.setElement(TRADING_SYSTEM, True)

    else:
        raise ValueError("Invalid 'scope_choice'.")


    # 2nd level filtering: by Basket, Multileg or OrdersAndRoutes
    if filter_choice:
        filter_by = request.getElement(FILTER_BY)

        if filter_choice.lower() == "basket":
            filter_by.setChoice(BASKET)
            filter_by.getElement(BASKET).appendValue(basket_name)

        elif filter_choice.lower() == "multileg":
            filter_by.setChoice(MULTILEG)
            filter_by.getElement(MULTILEG).appendValue(multileg_name)

        elif filter_choice.lower() == "ordersandroutes":
            filter_by.setChoice(ORDERS_AND_ROUTES)
            new_condition = filter_by.getElement(ORDERS_AND_ROUTES).appendElement()
            if order_id: new_condition.setElement(ORDER_ID, order_id)
            if route_id: new_condition.setElement(ROUTE_ID, route_id)

        else:
            raise ValueError("Invalid 'filter_choice'.")


    return request

