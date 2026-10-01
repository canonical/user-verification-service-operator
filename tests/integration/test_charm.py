#!/usr/bin/env python3
# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

import logging
from pathlib import Path

import jubilant
import requests
from tenacity import retry, stop_after_delay, wait_fixed

from tests.integration.constants import APP_NAME, LOCAL_CHARM, METADATA
from tests.integration.utils import all_active, any_error, get_unit_address

logger = logging.getLogger(__name__)


def test_build_and_deploy(
    juju: jubilant.Juju,
    charm_config: dict,
) -> None:
    resources = {"oci-image": METADATA["resources"]["oci-image"]["upstream-source"]}
    charm_path = Path(LOCAL_CHARM).resolve()
    juju.deploy(
        charm_path,
        resources=resources,
        app=APP_NAME,
        config=charm_config,
    )
    juju.wait(
        ready=all_active(APP_NAME),
        error=any_error(APP_NAME),
        timeout=10 * 60,
    )


def test_app_health(juju: jubilant.Juju, http_client: requests.Session) -> None:
    # The resource limits patch restarts the pod right after the unit first goes active,
    # and Juju keeps reporting that status until the new pod has run its hooks.
    @retry(wait=wait_fixed(5), stop=stop_after_delay(5 * 60), reraise=True)
    def check_status() -> None:
        public_address = get_unit_address(juju, APP_NAME, 0)
        resp = http_client.get(f"http://{public_address}:8080/api/v0/status", timeout=10)
        resp.raise_for_status()

    check_status()
