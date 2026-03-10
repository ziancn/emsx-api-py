"""
Wrapper method to create 'GetFills' request.
"""

import blpapi

from typing import List

from ..request_service_map import request_service_map


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


def get_fills(
        service: blpapi.Service,
        *,
        start_dt: str,
        end_dt: str,
        scope_choice: str,
        # Scope/Filter parameters
        team_name: str | None = None,
        uuids: int | List[int] | None = None,
        filter_choice: str | None = None,
        basket_name: str | None = None,
        multileg_name: str | None = None,
        order_id: int | None = None,
        route_id: int | None = None,
) -> blpapi.Request:
    """

    Args:
        service:
        start_dt: ISO 8601 format: 2017-02-08T00:00:00.000+00:00
        end_dt: ISO 8601 format: 2017-02-08T00:00:00.000+00:00
        scope_choice: Mandatory, 'Team', 'TradingSystem' or 'Uuid'
        team_name:
        uuids:
        filter_choice: Optional, 'Basket', 'Multileg' or 'OrdersAndRoutes'
        basket_name:
        multileg_name:
        order_id:
        route_id:

    Returns:

    """

    if service.name() not in request_service_map["GetFills"]:
        raise ValueError(f"Invalid service received. Service name: {service.name()}")

    request = service.createRequest("GetFills")
    request.set(FROM_DATETIME, start_dt)
    request.set(TO_DATETIME, end_dt)

    scope = request.getElement(SCOPE)


    # 1st level filtering: by Team, TradingSystem or Uuids
    match scope_choice.lower():
        case "team":
            scope.setChoice(TEAM)
            if team_name is not None:
                scope.setElement(TEAM, team_name)
            else:
                raise ValueError("Missing parameter 'team_name'.")
        case "uuids":
            scope.setChoice(UUIDS)
            if uuids is not None:
                if isinstance(uuids, int): uuids = [uuids]
                for uuid in uuids:
                    scope.getElement(UUIDS).appendValue(uuid)
        case "tradingsystem":
            # Note: Most of the time you will never use TradingSystem to filter.
            scope.setChoice(TRADING_SYSTEM)
            # If you encounter case where you really have different trading systems,
            # you need to pass the name of system to setElement. `True` is a mechanism
            # that tells server to link this UUID's current trading system.
            scope.setElement(TRADING_SYSTEM, True)
        case _:
            raise ValueError("Invalid 'scope_choice'.")


    # 2nd level filtering: by Basket, Multileg or OrdersAndRoutes
    if filter_choice is not None:
        filter_by = request.getElement(FILTER_BY)
        match filter_choice.lower():
            case "basket":
                filter_by.setChoice(BASKET)
                filter_by.getElement(BASKET).appendValue(basket_name)
            case "multileg":
                filter_by.setChoice(MULTILEG)
                filter_by.getElement(MULTILEG).appendValue(multileg_name)
            case "ordersandroutes":
                filter_by.setChoice(ORDERS_AND_ROUTES)
                new_condition = filter_by.getElement(ORDERS_AND_ROUTES).appendElement()
                if order_id: new_condition.setElement(ORDER_ID, order_id)
                if route_id: new_condition.setElement(ROUTE_ID, route_id)
            case _:
                raise ValueError("Invalid 'filter_choice'.")


    return request

