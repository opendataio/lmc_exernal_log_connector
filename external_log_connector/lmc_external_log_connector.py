# Copyright 2024-2025 Your Name.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
import asyncio
# Standard
from typing import List, Optional, no_type_check

# First Party (from lmcache)
from lmcache.logging import init_logger
from lmcache.utils import CacheEngineKey
from lmcache.v1.config import LMCacheEngineConfig
from lmcache.v1.memory_management import MemoryObj
from lmcache.v1.storage_backend.connector.base_connector import RemoteConnector

logger = init_logger(__name__)  # Inherit lmcache's logging configuration


class ExternalLogConnector(RemoteConnector):
    """
    A logging-enhanced connector extending RemoteConnector,
    with behavior identical to BlackholeConnector but with logging for each operation.
    """

    def __init__(self,
                 loop: asyncio.AbstractEventLoop,
                 local_cpu_backend: LocalCPUBackend,
                 config: Optional[LMCacheEngineConfig] = None):
        logger.info("[ExternalLogConnector] Initialization completed")

    async def exists(self, key: CacheEngineKey) -> bool:
        """Check if the key exists (logging-enhanced version)"""
        logger.debug(f"[ExternalLogConnector] Checking key existence: key={key}")
        # Behavior identical to BlackholeConnector: always returns False
        return False

    async def get(self, key: CacheEngineKey) -> Optional[MemoryObj]:
        """Get the value for the key (logging-enhanced version)"""
        logger.debug(f"[ExternalLogConnector] Getting key value: key={key}")
        # Behavior identical to BlackholeConnector: always returns None
        return None

    async def put(self, key: CacheEngineKey, memory_obj: MemoryObj):
        """Store the key-value pair (logging-enhanced version)"""
        logger.debug(f"[ExternalLogConnector] Storing key-value: key={key}, memory_obj={memory_obj}")
        # Behavior identical to BlackholeConnector: no actual operation
        pass

    @no_type_check
    async def list(self) -> List[str]:
        """List all keys (logging-enhanced version)"""
        logger.debug("[ExternalLogConnector] Listing all keys")
        # Behavior identical to BlackholeConnector: returns an empty list
        return []

    async def close(self):
        """Close the connector (logging-enhanced version)"""
        logger.info("[ExternalLogConnector] Connector closed")