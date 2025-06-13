# Copyright 2024-2025 Your Name.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
import asyncio
import time
# Standard
from typing import List, Optional, no_type_check

# First Party (from lmcache)
from lmcache.logging import init_logger
from lmcache.utils import CacheEngineKey
from lmcache.v1.config import LMCacheEngineConfig
from lmcache.v1.memory_management import MemoryObj
from lmcache.v1.storage_backend.connector.base_connector import RemoteConnector
from lmcache.v1.storage_backend.local_cpu_backend import LocalCPUBackend

logger = init_logger(__name__)

from enum import Enum, auto

class HealthState(Enum):
    HEALTHY = (0, "healthy")
    UNHEALTHY = (1000, "unhealthy")
    STUCK = (-1, "stuck")

    def __init__(self, code, description):
        self.code = code
        self.description = description

class ExternalLogConnector(RemoteConnector):
    """
    A logging-enhanced connector extending RemoteConnector,
    with behavior identical to BlackholeConnector but with logging for each operation.
    """

    def __init__(self,
                 loop: asyncio.AbstractEventLoop,
                 local_cpu_backend: LocalCPUBackend,
                 config: Optional[LMCacheEngineConfig] = None):
        self._support_ping =  (
            config.extra_config is not None
            and config.extra_config.get("ext_log_connector_support_ping", False)
        )
        self._state_change_interval =  (
            config.extra_config.get("ext_log_connector_health_interval", 0.0) if config.extra_config is not None else 0.0
        )
        self._stuck_time = (
            config.extra_config.get("ext_log_connector_stuck_time", 0.0) if config.extra_config is not None else 0.0
        )
        self._last_state_change_time = 0.0
        # Define state sequence: HEALTHY -> UNHEALTHY -> HEALTHY -> STUCK
        self._states = [
            HealthState.HEALTHY,
            HealthState.UNHEALTHY,
            HealthState.HEALTHY,
            HealthState.STUCK
        ]
        self._state_index = 0
        logger.info(f"[ExternalLogConnector] Initialization completed，"
                    f"support_ping: {self._support_ping}, "
                    f"state_change_interval_ms: {self._state_change_interval}, "
                    f"stuck_time_ms: {self._stuck_time}")

    async def exists(self, key: CacheEngineKey) -> bool:
        """Check if the key exists (logging-enhanced version)"""
        logger.info(f"[ExternalLogConnector] Checking key existence: key={key}")
        # Behavior identical to BlackholeConnector: always returns False
        return False

    async def get(self, key: CacheEngineKey) -> Optional[MemoryObj]:
        """Get the value for the key (logging-enhanced version)"""
        logger.info(f"[ExternalLogConnector] Getting key value: key={key}")
        # Behavior identical to BlackholeConnector: always returns None
        return None

    async def put(self, key: CacheEngineKey, memory_obj: MemoryObj):
        """Store the key-value pair (logging-enhanced version)"""
        logger.info(f"[ExternalLogConnector] Storing key-value: key={key}, memory_obj={memory_obj}")
        # Behavior identical to BlackholeConnector: no actual operation
        pass

    @no_type_check
    async def list(self) -> List[str]:
        """List all keys (logging-enhanced version)"""
        logger.info("[ExternalLogConnector] Listing all keys")
        # Behavior identical to BlackholeConnector: returns an empty list
        return []

    async def close(self):
        """Close the connector (logging-enhanced version)"""
        logger.info("[ExternalLogConnector] Connector closed")

    def support_ping(self) -> bool:
        return self._support_ping

    async def ping(self) -> int:
        if self._state_change_interval > 0:
            current_time = time.time()
            if current_time - self._last_state_change_time >= self._state_change_interval:
                self._last_state_change_time = current_time
                # Move to next state in sequence
                self._state_index = (self._state_index + 1) % len(self._states)
                state = self._states[self._state_index]

                # Sleep if entering stuck state
                if state == HealthState.STUCK and self._stuck_time > 0:
                    await asyncio.sleep(self._stuck_time)

                logger.warn(f"[ExternalLogConnector] State changed: {state.description}")
                return state.code

        # Return current state
        state = self._states[self._state_index]
        logger.info(f"[ExternalLogConnector] State kept: {state.description}")
        return state.code