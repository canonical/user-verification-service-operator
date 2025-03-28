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
        mocked_open_port: MagicMock,
        mocked_charm_holistic_handler: MagicMock,
        mocked_workload_service_version: MagicMock,
    ) -> None:
        ctx = testing.Context(UserVerificationServiceOperatorCharm)
        container = testing.Container("user-verification-service", can_connect=True)
        state_in = testing.State(containers={container})

        state_out = ctx.run(ctx.on.config_changed(), state_in)

        assert state_out.unit_status == testing.ActiveStatus()
        mocked_charm_holistic_handler.assert_called_once()
