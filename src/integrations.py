# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

import base64
import json
import logging
from dataclasses import dataclass, field, fields
from urllib.parse import urlparse

from charms.identity_platform_login_ui_operator.v0.login_ui_endpoints import (
    LoginUIEndpointsProvider,
    LoginUIEndpointsRequirer,
    LoginUIProviderData,
)
from charms.kratos.v0.kratos_registration_webhook import (
    KratosRegistrationWebhookProvider,
    ProviderData,
)
from charms.tempo_coordinator_k8s.v0.tracing import TracingEndpointRequirer
from charms.traefik_k8s.v0.traefik_route import TraefikRouteRequirer
from jinja2 import Template
from pydantic import AnyHttpUrl

from configs import ServiceConfigs
from constants import PORT, REGISTRATION_UI_INTEGRATION_NAME, REGISTRATION_WEBHOOK_INTEGRATION_NAME
from env_vars import EnvVars

logger = logging.getLogger(__name__)

WebhookBody = base64.b64encode(b"""function(ctx) {
  email: ctx.identity.traits.email
}""").decode()


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

        if not login_ui_endpoints:
            return cls()

        return dataclass_from_dict(cls, **login_ui_endpoints)


class UIEndpointIntegration:
    def __init__(self, requirer: LoginUIEndpointsProvider) -> None:
        self._requirer = requirer

    def is_ready(self) -> bool:
        rel = self._requirer._charm.model.get_relation(REGISTRATION_UI_INTEGRATION_NAME)
        return rel and rel.active

    def update_relation_data(self, ingress_url: str):
        self._requirer.send_endpoints_relation_data(
            LoginUIProviderData(registration_url=ingress_url)
        )


@dataclass(frozen=True, slots=True)
class IngressData:
    """The data source from the internal-ingress integration."""

    endpoint: AnyHttpUrl
    config: dict = field(default_factory=dict)

    def to_env_vars(self) -> ServiceConfigs:
        return {"UI_BASE_URL": str(self.endpoint)}

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


class KratosRegistrationWebhookIntegration:
    def __init__(self, requirer: KratosRegistrationWebhookProvider) -> None:
        self._requirer = requirer

    def is_ready(self) -> bool:
        rel = self._requirer._charm.model.get_relation(REGISTRATION_WEBHOOK_INTEGRATION_NAME)
        return rel and rel.active

    def update_relation_data(self, webhook_url: str, api_token: str):
        self._requirer.update_relations_app_data(
            ProviderData(
                url=webhook_url,
                body=f"base64://{WebhookBody}",
                method="POST",
                emit_analytics_event=False,
                response_ignore=False,
                response_parse=True,
                auth_config_name="Authorization",
                auth_config_value=api_token,
                auth_config_in="header",
            )
        )


@dataclass(frozen=True)
class TracingData:
    """The data source from the tracing integration."""

    is_ready: bool = False
    http_endpoint: str = ""

    def to_env_vars(self) -> EnvVars:
        return {
            "TRACING_ENABLED": self.is_ready,
            "OTEL_HTTP_ENDPOINT": self.http_endpoint,
        }

    @classmethod
    def load(cls, requirer: TracingEndpointRequirer) -> "TracingData":
        if not (is_ready := requirer.is_ready()):
            return TracingData()

        http_endpoint = urlparse(requirer.get_endpoint("otlp_http"))

        return TracingData(
            is_ready=is_ready,
            http_endpoint=http_endpoint.geturl().replace(f"{http_endpoint.scheme}://", "", 1),  # type: ignore[arg-type]
        )
