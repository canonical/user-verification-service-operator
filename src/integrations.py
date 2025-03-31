# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

import json
import logging
from dataclasses import dataclass, field, fields
from typing import Any, Type, TypeAlias, Union

from charms.identity_platform_login_ui_operator.v0.login_ui_endpoints import (
    LoginUIEndpointsRequirer,
)
from charms.traefik_route_k8s.v0.traefik_route import TraefikRouteRequirer
from jinja2 import Template
from pydantic import AnyHttpUrl

from configs import ServiceConfigs
from constants import PORT

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


@dataclass(frozen=True, slots=True)
class IngressData:
    """The data source from the internal-ingress integration."""

    endpoint: AnyHttpUrl
    config: dict = field(default_factory=dict)

    @classmethod
    def load(cls, requirer: TraefikRouteRequirer) -> "IngressData":
        model, app = requirer._charm.model.name, requirer._charm.app.name
        external_host = requirer.external_host
        external_endpoint = f"{requirer.scheme}://{external_host}/{model}-{app}"

        with open("templates/ingress.json.j2", "r") as file:
            template = Template(file.read())

        ingress_config = json.loads(
            template.render(
                model=model,
                app=app,
                port=PORT,
                external_host=external_host,
            )
        )

        endpoint = AnyHttpUrl(
            external_endpoint
            if external_host
            else f"http://{app}.{model}.svc.cluster.local:{PORT}"
        )

        return cls(
            endpoint=endpoint,
            config=ingress_config,
        )
