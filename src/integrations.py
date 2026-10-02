# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

import base64
import logging
from dataclasses import dataclass
from urllib.parse import urlparse

from charms.kratos.v0.kratos_registration_webhook import (
    KratosRegistrationWebhookProvider,
    ProviderData,
)
from charms.tempo_coordinator_k8s.v0.tracing import TracingEndpointRequirer

from constants import REGISTRATION_WEBHOOK_INTEGRATION_NAME
from env_vars import EnvVars

logger = logging.getLogger(__name__)

WebhookBody = base64.b64encode(b"""function(ctx) {
  email: ctx.identity.traits.email
}""").decode()


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
                weight=0,
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
