# emsx-api-py


A lightweight, modular Python client framework for integrating with Bloomberg EMSX services (via `blpapi`). `emsx-api-py` provides a session manager that handles the blpapi session lifecycle, request/response correlation, and a plugin-style module system so you can attach monitoring, logging, or business logic handlers. Typical use-cases include subscribing to EMSX streams (orders/routes), issuing EMSX requests (create/cancel orders, get fills), and building thin adapters for trading systems.

> NOTE: This package assumes you have a working Bloomberg `blpapi` environment and network connectivity to Bloomberg services.

## Features

- Simpler API calls with wrapper
- Modular design around session manager
- Modern Python syntax examples
- Buyside-request's POV adjusted structure

## Quick start

Prerequisites

- Python 3.12+
- `blpapi` installed and configured for your environment

Minimal example:

```python
from emsx_api_py import SessionManager
from emsx_api_py.modules import StatusMonitor, DemoModule

sm = SessionManager()
sm.register_module(StatusMonitor()) # Logs status
sm.register_module(DemoModule())    # Subscribes and logs heartbeat
sm.start_async()

try:
    print("Press ENTER to stop...")
    input()
finally:
    sm.session.stop()
```

## Acknowledgement

Examples and API usages developed are largely based on the [tkim/emsx_api_repository](https://github.com/tkim/emsx_api_repository).
