"""
This example creates BrokerSpec request.
"""

import blpapi
import logging

from emsx_api_py.session_manager import SessionManager
from emsx_api_py.modules import StatusMonitor
from emsx_api_py.requests.buyside.get_broker_spec_for_uuid import broker_spec


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main():
    # Session manager instance
    session_manager = SessionManager()
    # Modules
    status_mon = StatusMonitor()    # Log status related event/message
    # Register modules
    session_manager.register_module(status_mon)

    # Start
    session_manager.start()

    # Request and Response handler
    d_service = "//blp/emsx.brokerspec"
    session = session_manager.session
    session.openService(d_service)
    service_opened = session.getService(d_service)

    new_request = broker_spec(
        service_opened,
        trader_uuid = 12345678      # Note: Replace with your actual trader UUID here
    )

    def temp_handler(msg: blpapi.Message, session: blpapi.Session):
        brokers = msg.getElement(blpapi.Name("brokers"))
        num = brokers.numValues()
        print(f"Number of brokers: {num}")
        for broker in brokers.values():
            code = broker.getElement("code").getValue()
            asset_class = broker.getElement("assetClass").getValue()

            if broker.hasElement("strategyFixTag"):
                tag = broker.getElement("strategyFixTag").getValue()
                print(f"\nBroker code: {code}\tclass: {asset_class}\ttag: {tag}")

                strats = broker.getElement("strategies")
                num_strats = strats.numValues()

                print(f"\tNo. of Strategies: {num_strats}")

                for strat in strats.values():
                    name = strat.getElement("name").getValue()
                    fix_val = strat.getElement("fixValue").getValue()

                    print(f"\n\tStrategy Name: {name}\tFix Value: {fix_val}")

                    parameters = strat.getElement("parameters")
                    num_params = parameters.numValues()

                    print(f"\t\tNo. of Parameters: {num_params}\n")

                    for param in parameters.values():
                        pname = param.getElement("name").getValue()
                        tag = param.getElement("fixTag").getValue()
                        required = param.getElement("isRequired").getValue()
                        replaceable = param.getElement("isReplaceable").getValue()

                        print(
                            f"\t\tParameter: {pname}\tTag: {tag}\t"
                            f"Required: {required}\tReplaceable: {replaceable}"
                        )

                        type_elem = param.getElement("type").getElement(0)
                        type_name = type_elem.name()

                        vals = ""

                        match type_name:
                            case "enumeration":
                                enumerators = type_elem.getElement("enumerators")
                                vals = ", ".join(
                                    f"{enum.getElement('name').getValue()}[{enum.getElement('fixValue').getValue()}]"
                                    for enum in enumerators.values()
                                )

                            case "range":
                                rng = type_elem
                                mn = rng.getElement("min").getValue()
                                mx = rng.getElement("max").getValue()
                                st = rng.getElement("step").getValue()
                                vals = f"min:{mn} max:{mx} step:{st}"

                            case "string":
                                poss_vals = type_elem.getElement("possibleValues")
                                vals = ", ".join(
                                    str(val) for val in poss_vals.values()
                                )

                        if vals:
                            print(f"\t\t\tType: {type_name} ({vals})")
                        else:
                            print(f"\t\t\tType: {type_name}")

            else:
                print(f"\nBroker code: {code}\tclass: {asset_class}")
                print("\tNo strategies\n")

    # Send request
    session_manager.send_request(new_request, temp_handler)

    # Block main thread
    try:
        print("Press ENTER to quit")
        input()
    finally:
        session_manager.session.stop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Stopped by user")





