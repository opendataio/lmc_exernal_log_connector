# external-log-connector: Logging-enhanced Remote Connector

A `RemoteConnector` extension module based on `lmcache`, with behavior identical to `BlackholeConnector` but with detailed logging for each operation.

## Features
- Fully compatible with `lmcache`'s `RemoteConnector` interface
- Structured logging added for each method (`exists`/`get`/`put`/`list`/`close`/`ping`)
- Behavior identical to `BlackholeConnector` (no actual data storage)

## Installation
### Install from pypi

```
pip install external_log_connector
```

### Build whl package from source
```bash
# Clone the project and enter the directory
cd external_log_connector

# Build the whl file (will be generated in the dist/ directory)
sh ./dev/build_whl.sh
# Or you can build and upload it into pypi by
#  sh ./dev/publish.sh <NEW_VERSION>
# Or you want to upload generated whl into pypi by
#  twine upload dist/*

pip install dist/*.whl
```

## How to use

```yaml
# lmcache.yaml
chunk_size: 256
local_device: "cpu"
local_cpu: False
max_local_cpu_size: 5
remote_url: "external://host:0/external_log_connector.lmc_external_log_connector/?connector_name=ExternalLogConnector"
remote_serde: "naive"
pipelined_backend: False
extra_config:
  ext_log_connector_support_ping: True
  ext_log_connector_health_interval: 10.0
  ext_log_connector_stuck_time: 6.0
```

```shell
LMCACHE_USE_EXPERIMENTAL=True LMCACHE_TRACK_USAGE=false \
VLLM_MLA_DISABLE=0 VLLM_USE_V1=1 LMCACHE_CONFIG_FILE=./lmcache.yaml \
vllm serve /disc/data1/deepseek/DeepSeek-V2-Lite-Chat/ \
           --trust-remote-code \
           --served-model-name vllm_cpu_offload \
           --max-model-len 32768 \
           --max-seq-len-to-capture 10000 \
           --max-num-seqs 64 \
           --gpu-memory-utilization 0.9 \
           --host 0.0.0.0 \
           -tp 1 \
           --kv-transfer-config '{"kv_connector":"LMCacheConnectorV1","kv_role":"kv_both","kv_parallel_size":2}'
```
