# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

from unittest.mock import MagicMock

from ops import testing

from charm import UserVerificationServiceOperatorCharm


class TestPebbleReadyEvent:
    def test_when_event_emitted(
        self,
        mocked_open_port: MagicMock,
        mocked_charm_holistic_handler: MagicMock,
        mocked_workload_service_version: MagicMock,
    ) -> None:
        ctx = testing.Context(UserVerificationServiceOperatorCharm)
        container = testing.Container("user-verification-service", can_connect=True)
        state_in = testing.State(containers={container})

        state_out = ctx.run(ctx.on.pebble_ready(container), state_in)

        assert state_out.unit_status == testing.ActiveStatus()
        mocked_open_port.assert_called_once()
        mocked_charm_holistic_handler.assert_called_once()
        assert state_out.workload_version == mocked_workload_service_version.return_value


class TestConfigChangedEvent:
    def test_when_event_emitted(
        self,
        mocked_charm_holistic_handler: MagicMock,
    ) -> None:
        ctx = testing.Context(UserVerificationServiceOperatorCharm)
        container = testing.Container("user-verification-service", can_connect=True)
        state_in = testing.State(containers={container})

        state_out = ctx.run(ctx.on.config_changed(), state_in)

        assert state_out.unit_status == testing.ActiveStatus()
        mocked_charm_holistic_handler.assert_called_once()


class TestHolisticHandler:
    def test_when_container_not_connected(
        self,
        mocked_event: MagicMock,
    ) -> None:
        ctx = testing.Context(UserVerificationServiceOperatorCharm)
        container = testing.Container("user-verification-service", can_connect=False)
        state_in = testing.State(containers={container})

        # We abuse the config_changed event, to run the unit tests on holistic_handler.
        # Scenario does not provide us with a way to
        state_out = ctx.run(ctx.on.config_changed(), state_in)

        assert state_out.unit_status == testing.WaitingStatus("Container is not connected yet")

    def test_when_all_conditions_satisfied(
        self,
        mocked_event: MagicMock,
        login_ui_integration_data: dict,
    ) -> None:
        ctx = testing.Context(UserVerificationServiceOperatorCharm)
        container = testing.Container("user-verification-service", can_connect=True)
        login_ui_relation = testing.Relation(
            endpoint="ui-endpoint-info",
            interface="login_ui_endpoints",
            remote_app_name="login-ui",
            remote_app_data=login_ui_integration_data,
        )
        state_in = testing.State(containers={container}, relations=[login_ui_relation])

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
            "ERROR_UI_URL": login_ui_integration_data["oidc_error_url"],
            "SUPPORT_EMAIL": "http://place-holder",
            "DIRECTORY_API_URL": "http://place-holder",
        }
