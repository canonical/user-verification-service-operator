# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

import logging
from dataclasses import dataclass, fields
from typing import Any, Type, TypeAlias, Union

from charms.identity_platform_login_ui_operator.v0.login_ui_endpoints import (
    LoginUIEndpointsRequirer,
)

from configs import ServiceConfigs

logger = logging.getLogger(__name__)

JsonSerializable: TypeAlias = Union[dict[str, Any], list[Any], int, str, float, bool, Type[None]]


def dataclass_from_dict(cls, **kwargs):
    fs = {field.name for field in fields(cls)}
    return cls(**{k: v for k, v in kwargs.items() if k in fs})


@dataclass(frozen=True, slots=True)
class LoginUIEndpointData:
    """The data source from the login-ui integration."""

    oidc_error_url: str = ""

    def to_env_vars(self) -> ServiceConfigs:
        return {"ERROR_UI_URL": self.oidc_error_url}

    @classmethod
    def load(cls, requirer: LoginUIEndpointsRequirer) -> "LoginUIEndpointData":
        try:
            login_ui_endpoints = requirer.get_login_ui_endpoints()
        except Exception as exc:
            logger.error("Failed to fetch the login ui endpoints: %s", exc)
            return cls()

        return dataclass_from_dict(cls, **login_ui_endpoints)
