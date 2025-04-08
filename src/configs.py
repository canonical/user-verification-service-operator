# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.

from typing import Any, Mapping, TypeAlias

from ops.model import ConfigData

from env_vars import EnvVars

ServiceConfigs: TypeAlias = Mapping[str, Any]


class CharmConfig:
    """A class representing the data source of charm configurations."""

    def __init__(self, config: ConfigData) -> None:
        self._config = config

    def to_env_vars(self) -> EnvVars:
        return {
            "LOG_LEVEL": self._config["log_level"].upper(),
            "SUPPORT_EMAIL": self._config.get("support_email", ""),
        }
