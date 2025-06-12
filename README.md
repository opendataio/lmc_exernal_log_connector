# external-log-connector: Logging-enhanced Remote Connector

A `RemoteConnector` extension module based on `lmcache`, with behavior identical to `BlackholeConnector` but with detailed logging for each operation.

## Features
- Fully compatible with `lmcache`'s `RemoteConnector` interface
- Structured logging added for each method (`exists`/`get`/`put`/`list`/`close`)
- Behavior identical to `BlackholeConnector` (no actual data storage)

## Installation
### Build whl package from source
```bash
# Clone the project and enter the directory
cd external_log_connector

# Build the whl file (will be generated in the dist/ directory)
./build_whl.sh
```
