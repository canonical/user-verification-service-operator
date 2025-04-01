#!/usr/bin/env python3
# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""A Juju charm for Identity Platform User Verification Service."""

import logging

import ops

from configs import CharmConfig
from constants import WORKLOAD_CONTAINER
from exceptions import PebbleError
from services import PebbleService, WorkloadService
from utils import EVENT_DEFER_CONDITIONS, NOOP_CONDITIONS

logger = logging.getLogger(__name__)


class UserVerificationServiceOperatorCharm(ops.CharmBase):
    """Charm the application."""

    def __init__(self, framework: ops.Framework):
        super().__init__(framework)

        self._workload_service = WorkloadService(self.unit)
        self._pebble_service = PebbleService(self.unit)

        framework.observe(self.on.user_verification_service_pebble_ready, self._on_pebble_ready)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.collect_unit_status, self._on_collect_status)

    def _on_config_changed(self, event: ops.ConfigChangedEvent):
        self._holistic_handler(event)

    def _on_pebble_ready(self, event: ops.PebbleReadyEvent):
        self._workload_service.open_port()
        self._holistic_handler(event)

        self._workload_service.set_version()

    def _holistic_handler(self, event: ops.EventBase) -> None:
        if not all(condition(self) for condition in NOOP_CONDITIONS):
            return

        if not all(condition(self) for condition in EVENT_DEFER_CONDITIONS):
            event.defer()
            return

        try:
            self._pebble_service.plan(self._pebble_layer)
        except PebbleError:
            logger.error(
                f"Failed to plan pebble layer, please check the {WORKLOAD_CONTAINER} container logs"
            )
            raise

    @property
    def _pebble_layer(self) -> ops.pebble.Layer:
        charm_config = CharmConfig(self.config)

        return self._pebble_service.render_pebble_layer(
            charm_config,
        )

    def _on_collect_status(self, event: ops.CollectStatusEvent) -> None:
        event.add_status(ops.ActiveStatus())


if __name__ == "__main__":  # pragma: nocover
    ops.main(UserVerificationServiceOperatorCharm)
