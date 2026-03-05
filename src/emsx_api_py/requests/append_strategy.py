"""
This method appends strategy parameters to a route request.
"""

import blpapi

from typing import List, Tuple


# blpapi names
EMSX_BROKER                    = blpapi.Name("EMSX_BROKER")
EMSX_STRATEGY_PARAMS           = blpapi.Name("EMSX_STRATEGY_PARAMS")
EMSX_STRATEGY_NAME             = blpapi.Name("EMSX_STRATEGY_NAME")
EMSX_STRATEGY_FIELDS           = blpapi.Name("EMSX_STRATEGY_FIELDS")
EMSX_STRATEGY_FIELD_INDICATORS = blpapi.Name("EMSX_STRATEGY_FIELD_INDICATORS")
EMSX_FIELD_DATA                = blpapi.Name("EMSX_FIELD_DATA")
EMSX_FIELD_INDICATOR           = blpapi.Name("EMSX_FIELD_INDICATOR")


def append_strategy(
        request: blpapi.Request,
        strategy_name: str,
        parameters: List[Tuple[any, int]]
) -> None:
    """
    Append strategy parameters to a route request.
    Recommended to be used after creating a raw route request using ``route_ex_raw`` method.

    Args:
        request:
        strategy_name:
        parameters: List of tuples where tuples contain
                    1). strategy parameter value
                    2). indicator： ``0`` means this field carries value and ``1`` means skip this field

    """
    # Todo: check if strategy is valid for this broker
    strategy = request.getElement(EMSX_STRATEGY_PARAMS)     # Create a strategy param object
    strategy.setElement(EMSX_STRATEGY_NAME, strategy_name)  # Set strategy

    data      = strategy.getElement(EMSX_STRATEGY_FIELDS)               # Param data value array
    indicator = strategy.getElement(EMSX_STRATEGY_FIELD_INDICATORS)     # Indicator array

    for i in parameters:
        data.appendElement().setElement(EMSX_FIELD_DATA, i[0])
        indicator.appendElement().setElement(EMSX_FIELD_INDICATOR, i[1])

    return


if __name__ == "__main__":
    # Example usage and explanation
    # i.e. Portion of Volume provided by the broker is called "VolinLine"
    # And you have below strategy info from "GetBrokerStrategyInfoWithAssetClass" request
    # VolinLine
    # MESSAGE TYPE: GetBrokerStrategyInfoWithAssetClass
    # EMSX_STRATEGY_INFO: Start Time, 0,
    # EMSX_STRATEGY_INFO: End Time, 0,
    # EMSX_STRATEGY_INFO: AuctPartRate, 0,
    # EMSX_STRATEGY_INFO: Min%Volume, 0,
    # EMSX_STRATEGY_INFO: Max%Volume, 0,
    # EMSX_STRATEGY_INFO: Style, 0,
    # EMSX_STRATEGY_INFO: SOR, 0,
    # EMSX_STRATEGY_INFO: IWould Px, 0,
    # EMSX_STRATEGY_INFO: IWouldOrder%, 0,
    # EMSX_STRATEGY_INFO: IWould Max%, 0,
    # EMSX_STRATEGY_INFO: DlimitPxBk, 0,
    # EMSX_STRATEGY_INFO: DlimitPx%, 0,
    # EMSX_STRATEGY_INFO: DWldPxBk, 0,
    # EMSX_STRATEGY_INFO: DWldPx%, 0,
    # EMSX_STRATEGY_INFO: Algo2 ID, 0,
    # EMSX_STRATEGY_INFO: Algo2 Order%, 0,
    # EMSX_STRATEGY_INFO: Algo2 Max%, 0,
    # EMSX_STRATEGY_INFO: Algo2 Limit, 0,
    # EMSX_STRATEGY_INFO: Algo2 Time, 0,
    # EMSX_STRATEGY_INFO: Algo2 Sw Px, 0,
    # We will set start time, end time, max% volume
    # The parameters we pass to the wrapper method will look like:
    params = [
        ("09:30:00", 0),    # Start time, 0 means the field carries value
        ("15:00:00", 0),    # End time, 0 means the field carries value
        (""        , 1),    # AuctPartRate, 1 means the field should be ignored
        (0         , 1),    # Min%Volume, 1 means the field should be ignored
        (25        , 0),    # Max%Volume, 0 means the field carries value
    ]

    # Assume we have a raw(without strategy params) RoutEx request here
    # request: blpapi.Request
    # append_strategy(request, "VolinLine", params)
    ...



