# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

from typing import List
from unittest.mock import MagicMock, patch

import pytest
from ops import StatusBase, testing

from charm import UserVerificationServiceOperatorCharm
from constants import LOGIN_UI_INTEGRATION_NAME


class TestPebbleReadyEvent:
    def test_when_event_emitted(
        self,
        mocked_open_port: MagicMock,
        mocked_charm_holistic_handler: MagicMock,
        mocked_workload_service_version: MagicMock,
        login_ui_integration: testing.Relation,
        mocked_secrets: List[testing.Secret],
        charm_config: dict,
    ) -> None:
        ctx = testing.Context(UserVerificationServiceOperatorCharm)
        container = testing.Container("user-verification-service", can_connect=True)
        state_in = testing.State(
            containers={container},
            relations=[login_ui_integration],
            config=charm_config,
            secrets=mocked_secrets,
        )

        state_out = ctx.run(ctx.on.pebble_ready(container), state_in)

        assert state_out.unit_status == testing.ActiveStatus()
        mocked_open_port.assert_called_once()
        mocked_charm_holistic_handler.assert_called_once()
        assert state_out.workload_version == mocked_workload_service_version.return_value


class TestConfigChangedEvent:
    def test_when_config_missing(
        self,
        login_ui_integration: testing.Relation,
        mocked_secrets: List[testing.Secret],
    ) -> None:
        ctx = testing.Context(UserVerificationServiceOperatorCharm)
        container = testing.Container("user-verification-service", can_connect=True)
        state_in = testing.State(
            containers={container}, relations=[login_ui_integration], secrets=mocked_secrets
        )

        state_out = ctx.run(ctx.on.config_changed(), state_in)

        assert isinstance(state_out.unit_status, testing.BlockedStatus)

    def test_when_event_emitted(
        self,
        mocked_charm_holistic_handler: MagicMock,
        login_ui_integration: testing.Relation,
        mocked_secrets: List[testing.Secret],
        charm_config: dict,
    ) -> None:
        ctx = testing.Context(UserVerificationServiceOperatorCharm)
        container = testing.Container("user-verification-service", can_connect=True)
        state_in = testing.State(
            containers={container},
            relations=[login_ui_integration],
            config=charm_config,
            secrets=mocked_secrets,
        )

        state_out = ctx.run(ctx.on.config_changed(), state_in)

        assert state_out.unit_status == testing.ActiveStatus()
        mocked_charm_holistic_handler.assert_called_once()


class TestPublicIngressReadyEvent:
    def test_when_event_emitted(
        self,
        ingress_integration: testing.Relation,
        login_ui_integration: testing.Relation,
        mocked_secrets: List[testing.Secret],
        charm_config: dict,
    ) -> None:
        ctx = testing.Context(UserVerificationServiceOperatorCharm)
        container = testing.Container("user-verification-service", can_connect=True)
        state_in = testing.State(
            containers={container},
            relations=[ingress_integration, login_ui_integration],
            config=charm_config,
            secrets=mocked_secrets,
        )

        state_out = ctx.run(ctx.on.relation_joined(ingress_integration), state_in)

        assert state_out.unit_status == testing.ActiveStatus()


class TestPublicIngressRevokedEvent:
    def test_when_event_emitted(
        self,
        ingress_integration: testing.Relation,
        login_ui_integration: testing.Relation,
        mocked_secrets: List[testing.Secret],
        charm_config: dict,
    ) -> None:
        ctx = testing.Context(UserVerificationServiceOperatorCharm)
        container = testing.Container("user-verification-service", can_connect=True)
        state_in = testing.State(
            containers={container},
            relations=[ingress_integration, login_ui_integration],
            config=charm_config,
            secrets=mocked_secrets,
        )

        state_out = ctx.run(ctx.on.relation_broken(ingress_integration), state_in)

        assert state_out.unit_status == testing.ActiveStatus()


class TestHolisticHandler:
    def test_when_container_not_connected(
        self,
        login_ui_integration: testing.Relation,
        charm_config: dict,
    ) -> None:
        ctx = testing.Context(UserVerificationServiceOperatorCharm)
        container = testing.Container("user-verification-service", can_connect=False)
        state_in = testing.State(
            containers={container}, relations=[login_ui_integration], config=charm_config
        )

        # We abuse the config_changed event, to run the unit tests on holistic_handler.
        # Scenario does not provide us with a way to
        state_out = ctx.run(ctx.on.config_changed(), state_in)

        assert state_out.unit_status == testing.WaitingStatus("Container is not connected yet")

    def test_when_all_conditions_satisfied(
        self,
        login_ui_integration: testing.Relation,
        ingress_integration: testing.Relation,
        mocked_secrets: List[testing.Secret],
        charm_config: dict,
        support_email: str,
        api_token: str,
        directory_api_url: str,
        directory_api_token: testing.Secret,
    ) -> None:
        ctx = testing.Context(UserVerificationServiceOperatorCharm)
        container = testing.Container("user-verification-service", can_connect=True)
        state_in = testing.State(
            containers={container},
            relations=[login_ui_integration, ingress_integration],
            config=charm_config,
            leader=True,
            secrets=mocked_secrets,
        )

        # We abuse the config_changed event, to run the unit tests on holistic_handler.
        # Scenario does not provide us with a way to
        state_out = ctx.run(ctx.on.config_changed(), state_in)

        layer = state_out.get_container("user-verification-service").layers[
            "user-verification-service"
        ]
        assert state_out.unit_status == testing.ActiveStatus()
        assert layer.services.get("user-verification-service").environment == {
            "OTEL_HTTP_ENDPOINT": "",
            "OTEL_GRPC_ENDPOINT": "",
            "TRACING_ENABLED": False,
            "LOG_LEVEL": "INFO",
            "PORT": "8080",
            "ERROR_UI_URL": login_ui_integration.remote_app_data["oidc_error_url"],
            "SUPPORT_EMAIL": support_email,
            "API_TOKEN": api_token,
            "DIRECTORY_API_URL": directory_api_url,
            "DIRECTORY_API_TOKEN": directory_api_token,
            "SKIP_TLS_VERIFICATION": False,
            "UI_BASE_URL": f"http://{ingress_integration.remote_app_data['external_host']}/{state_out.model.name}-user-verification-service",
        }


class TestCollectStatusEvent:
    def test_when_all_condition_satisfied(
        self,
        all_satisfied_conditions: MagicMock,
    ) -> None:
        ctx = testing.Context(UserVerificationServiceOperatorCharm)
        container = testing.Container("user-verification-service", can_connect=True)
        state_in = testing.State(containers={container})

        state_out = ctx.run(ctx.on.collect_unit_status(), state_in)

        assert state_out.unit_status == testing.ActiveStatus()

    @pytest.mark.parametrize(
        "condition, status, message",
        [
            ("container_connectivity", testing.WaitingStatus, "Container is not connected yet"),
            (
                "login_ui_integration_exists",
                testing.BlockedStatus,
                f"Missing integration {LOGIN_UI_INTEGRATION_NAME}",
            ),
        ],
    )
    def test_when_a_condition_failed(
        self,
        all_satisfied_conditions: MagicMock,
        condition: str,
        status: StatusBase,
        message: str,
    ) -> None:
        ctx = testing.Context(UserVerificationServiceOperatorCharm)
        container = testing.Container("user-verification-service", can_connect=True)
        state_in = testing.State(containers={container})

        with patch(f"charm.{condition}", return_value=False):
            state_out = ctx.run(ctx.on.collect_unit_status(), state_in)

        assert isinstance(state_out.unit_status, status)
        assert state_out.unit_status.message == message
