# emsx-api-py


A lightweight, modular Python client framework for integrating with Bloomberg EMSX services (via `blpapi`). `emsx-api-py` provides a session manager that handles the blpapi session lifecycle, request/response correlation, and a plugin-style module system so you can attach monitoring, logging, or business logic handlers. Typical use-cases include subscribing to EMSX streams (orders/routes), issuing EMSX requests (create/cancel orders, get fills), and building thin adapters for trading systems.

> NOTE: This package assumes you have a working Bloomberg `blpapi` environment and network connectivity to Bloomberg services.

## Features

- Wrappers that make API calls simpler
- Modular design
- Rewritten examples with more modern Python syntax
- Restructured documation that fits buyside-request's needs

## Quick start

Prerequisites

- Python 3.12+
- `blpapi` installed and configured for your environment

Minimal example:

```python
from emsx_api_py import SessionManager
from emsx_api_py.modules import StatusMonitor

sm = SessionManager()
sm.register_module(StatusMonitor())
sm.start_async()

try:
    print("Press ENTER to stop...")
    input()
finally:
    sm.session.stop()
```
