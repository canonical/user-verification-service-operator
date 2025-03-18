# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing

from ops import testing

from charm import UserVerificationServiceOperatorCharm


def test_pebble_ready():
    # Arrange:
    ctx = testing.Context(UserVerificationServiceOperatorCharm)
    container = testing.Container("user-verification-service", can_connect=True)
    state_in = testing.State(containers={container})

    # Act:
    state_out = ctx.run(ctx.on.pebble_ready(container), state_in)

    # Assert:
    assert state_out.unit_status == testing.ActiveStatus()
