#!/usr/bin/env python3
# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""A Juju charm for Identity Platform User Verification Service."""

import logging
from secrets import token_hex

import ops
from charms.grafana_k8s.v0.grafana_dashboard import GrafanaDashboardProvider
from charms.identity_platform_login_ui_operator.v0.login_ui_endpoints import (
    LoginUIEndpointsProvider,
    LoginUIEndpointsRequirer,
)
from charms.kratos.v0.kratos_registration_web_hook import (
    KratosRegistrationWebhookProvider,
)
from charms.loki_k8s.v1.loki_push_api import LogForwarder
from charms.prometheus_k8s.v0.prometheus_scrape import MetricsEndpointProvider
from charms.tempo_coordinator_k8s.v0.tracing import TracingEndpointRequirer
from charms.traefik_k8s.v0.traefik_route import TraefikRouteRequirer

from configs import CharmConfig
from constants import (
    API_TOKEN_SECRET_KEY,
    API_TOKEN_SECRET_LABEL,
    GRAFANA_DASHBOARD_INTEGRATION_NAME,
    INGRESS_INTEGRATION_NAME,
    LOGGING_RELATION_NAME,
    LOGIN_UI_INTEGRATION_NAME,
    PORT,
    PROMETHEUS_SCRAPE_INTEGRATION_NAME,
    REGISTRATION_UI_INTEGRATION_NAME,
    TEMPO_TRACING_INTEGRATION_NAME,
    WORKLOAD_CONTAINER,
)
from exceptions import PebbleError
from integrations import (
    IngressData,
    KratosRegistrationWebhookIntegration,
    LoginUIEndpointData,
    TracingData,
    UIEndpointIntegration,
)
from secret import Secrets
from services import PebbleService, WorkloadService
from utils import (
    EVENT_DEFER_CONDITIONS,
    NOOP_CONDITIONS,
    container_connectivity,
    leader_unit,
    login_ui_integration_exists,
)

logger = logging.getLogger(__name__)


class UserVerificationServiceOperatorCharm(ops.CharmBase):
    """Charm the application."""

    def __init__(self, framework: ops.Framework):
        super().__init__(framework)

        self._workload_service = WorkloadService(self.unit)
        self._pebble_service = PebbleService(self.unit)
        self._secrets = Secrets(self.model)

        self.login_ui_requirer = LoginUIEndpointsRequirer(
            self, relation_name=LOGIN_UI_INTEGRATION_NAME
        )
        self.registration_endpoints_provider = LoginUIEndpointsProvider(
            self, relation_name=REGISTRATION_UI_INTEGRATION_NAME
        )
        self.registration_endpoints_integration = UIEndpointIntegration(
            self.registration_endpoints_provider
        )

        self.kratos_registration_webhook = KratosRegistrationWebhookProvider(self)
        self.kratos_webhook_integration = KratosRegistrationWebhookIntegration(
            self.kratos_registration_webhook
        )

        self.ingress = TraefikRouteRequirer(
            self,
            self.model.get_relation(INGRESS_INTEGRATION_NAME),
            INGRESS_INTEGRATION_NAME,
            raw=True,
        )

        self.metrics_endpoint = MetricsEndpointProvider(
            self,
            relation_name=PROMETHEUS_SCRAPE_INTEGRATION_NAME,
            jobs=[
                {
                    "job_name": "user_verification_service_metrics",
                    "metrics_path": "/api/v0/metrics",
                    "static_configs": [
                        {
                            "targets": [f"*:{PORT}"],
                        }
                    ],
                }
            ],
        )

        # Loki logging relation
        self._log_forwarder = LogForwarder(self, relation_name=LOGGING_RELATION_NAME)

        self._grafana_dashboards = GrafanaDashboardProvider(
            self,
            relation_name=GRAFANA_DASHBOARD_INTEGRATION_NAME,
        )

        self.tracing_requirer = TracingEndpointRequirer(
            self, relation_name=TEMPO_TRACING_INTEGRATION_NAME, protocols=["otlp_http"]
        )

        framework.observe(self.on.user_verification_service_pebble_ready, self._on_pebble_ready)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.leader_elected, self._on_leader_elected)
        self.framework.observe(self.on.leader_settings_changed, self._on_leader_settings_changed)
        self.framework.observe(self.on.collect_unit_status, self._on_collect_status)

        self.framework.observe(
            self.on[LOGIN_UI_INTEGRATION_NAME].relation_joined, self._on_login_ui_changed
        )
        self.framework.observe(
            self.on[LOGIN_UI_INTEGRATION_NAME].relation_changed, self._on_login_ui_changed
        )
        self.framework.observe(
            self.on[LOGIN_UI_INTEGRATION_NAME].relation_broken, self._on_login_ui_changed
        )

        self.framework.observe(self.registration_endpoints_provider.on.ready, self._on_ui_ready)

        self.framework.observe(
            self.kratos_registration_webhook.on.ready, self._on_kratos_webhook_ready
        )

        # internal ingress
        self.framework.observe(
            self.ingress.on.ready,
            self._on_internal_ingress_changed,
        )

    @property
    def _pebble_layer(self) -> ops.pebble.Layer:
        charm_config = CharmConfig(self.config)
        return self._pebble_service.render_pebble_layer(
            LoginUIEndpointData.load(self.login_ui_requirer),
            TracingData.load(self.tracing_requirer),
            self._secrets,
            charm_config,
        )

    @property
    def _webhook_url(self) -> str:
        return f"http://{self.app.name}.{self.model.name}.svc.cluster.local:{PORT}/api/v0/verify"

    @property
    def _registration_url(self) -> str:
        return f"{IngressData.load(self.ingress).endpoint}/ui/registration_error"

    @leader_unit
    def _prepare_secrets(self) -> None:
        self._secrets[API_TOKEN_SECRET_LABEL] = {API_TOKEN_SECRET_KEY: token_hex(16)}

    @leader_unit
    def _on_internal_ingress_changed(self, event: ops.RelationEvent) -> None:
        if self.ingress.is_ready():
            ingress_config = IngressData.load(self.ingress).config
            self.ingress.submit_to_traefik(ingress_config)
        self._holistic_handler(event)

    def _on_leader_elected(self, event: ops.LeaderElectedEvent) -> None:
        self._holistic_handler(event)

    def _on_leader_settings_changed(self, event: ops.LeaderSettingsChangedEvent) -> None:
        self._holistic_handler(event)

    def _on_config_changed(self, event: ops.ConfigChangedEvent):
        self._holistic_handler(event)

    def _on_login_ui_changed(self, event: ops.RelationEvent):
        self._holistic_handler(event)

    def _on_pebble_ready(self, event: ops.PebbleReadyEvent):
        self._workload_service.open_port()
        self._holistic_handler(event)

        self._workload_service.set_version()

    def _on_kratos_webhook_ready(self, event: ops.RelationEvent) -> None:
        self._holistic_handler(event)

    def _on_ui_ready(self, event: ops.RelationEvent) -> None:
        self._holistic_handler(event)

    def _holistic_handler(self, event: ops.EventBase) -> None:
        if not all(condition(self) for condition in NOOP_CONDITIONS):
            return

        if not all(condition(self) for condition in EVENT_DEFER_CONDITIONS):
            event.defer()
            return

        if not self._secrets.is_ready():
            if not self.unit.is_leader():
                return
            self._prepare_secrets()

        if self.kratos_webhook_integration.is_ready():
            self.kratos_webhook_integration.update_relation_data(
                self._webhook_url,
                self._secrets.api_token,
            )

        if self.registration_endpoints_integration.is_ready():
            self.registration_endpoints_integration.update_relation_data(self._registration_url)

        try:
            self._pebble_service.plan(self._pebble_layer)
        except PebbleError:
            logger.error(
                f"Failed to plan pebble layer, please check the {WORKLOAD_CONTAINER} container logs"
            )
            raise

    def _on_collect_status(self, event: ops.CollectStatusEvent) -> None:
        if not container_connectivity(self):
            event.add_status(ops.WaitingStatus("Container is not connected yet"))

        if not login_ui_integration_exists(self):
            event.add_status(ops.BlockedStatus(f"Missing integration {LOGIN_UI_INTEGRATION_NAME}"))

        if not self._secrets.is_ready():
            event.add_status(ops.WaitingStatus("Waiting for secrets creation"))

        event.add_status(ops.ActiveStatus())


if __name__ == "__main__":  # pragma: nocover
    ops.main(UserVerificationServiceOperatorCharm)
