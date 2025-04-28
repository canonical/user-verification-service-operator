# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.

from typing import Any, Mapping, TypeAlias

from ops import ConfigData, Model

from constants import CONFIG_DIRECTORY_API_TOKEN_SECRET_KEY
from env_vars import EnvVars

ServiceConfigs: TypeAlias = Mapping[str, Any]


class CharmConfig:
    """A class representing the data source of charm configurations."""

    REQUIRED_KEYS = ["directory_api_url", "directory_api_token"]

    def __init__(self, config: ConfigData, model: Model) -> None:
        self._config = config
        self._model = model

    def _get_directory_api_token(self) -> str:
        secret_id = self._config["directory_api_token"]
        secret = self._model.get_secret(id=secret_id)
        return secret.get_content(refresh=True)[CONFIG_DIRECTORY_API_TOKEN_SECRET_KEY]

    def get_missing_config_keys(self) -> bool:
        return [k for k in self.REQUIRED_KEYS if not self._config.get(k)]

    def to_env_vars(self) -> EnvVars:
        return {
            "LOG_LEVEL": self._config["log_level"].upper(),
            "SUPPORT_EMAIL": self._config.get("support_email", ""),
            "DIRECTORY_API_URL": self._config["directory_api_url"],
            "DIRECTORY_API_TOKEN": self._get_directory_api_token(),
            "SKIP_TLS_VERIFICATION": self._config.get("skip_tls_verification", False),
        }
