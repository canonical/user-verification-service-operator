# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.

from typing import Any, List, Mapping, Tuple, TypeAlias

from ops import ConfigData, Model

from constants import CONFIG_CONSUMER_KEY_SECRET_KEY, CONFIG_CONSUMER_SECRET_SECRET_KEY
from env_vars import EnvVars

ServiceConfigs: TypeAlias = Mapping[str, Any]


class CharmConfig:
    """A class representing the data source of charm configurations."""

    REQUIRED_KEYS = ["salesforce_domain", "salesforce_consumer_secret"]

    def __init__(self, config: ConfigData, model: Model) -> None:
        self._config = config
        self._model = model

    def _get_salesforce_consumer_info(self) -> Tuple[str, str]:
        secret_id = self._config["salesforce_consumer_secret"]
        secret = self._model.get_secret(id=secret_id)
        content = secret.get_content(refresh=True)
        return content[CONFIG_CONSUMER_KEY_SECRET_KEY], content[CONFIG_CONSUMER_SECRET_SECRET_KEY]

    def get_missing_config_keys(self) -> List:
        if not self._config.get("salesforce_enabled"):
            return []
        return [k for k in self.REQUIRED_KEYS if not self._config.get(k)]

    def to_env_vars(self) -> EnvVars:
        env = {
            "LOG_LEVEL": self._config["log_level"].upper(),
            "SUPPORT_EMAIL": self._config.get("support_email", ""),
            "SALESFORCE_ENABLED": self._config.get("salesforce_enabled", True),
        }
        if self._config.get("salesforce_enabled"):
            consumer = self._get_salesforce_consumer_info()
            env.update({
                "SALESFORCE_CONSUMER_KEY": consumer[0],
                "SALESFORCE_CONSUMER_SECRET": consumer[1],
                "SALESFORCE_DOMAIN": self._config.get("salesforce_domain"),
            })
        return env
