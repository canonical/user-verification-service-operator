#!/usr/bin/env python3
# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

import logging
from pathlib import Path

import pytest
import requests
import yaml
from pytest_operator.plugin import OpsTest

logger = logging.getLogger(__name__)

METADATA = yaml.safe_load(Path("./charmcraft.yaml").read_text())
APP_NAME = METADATA["name"]
LOGIN_UI_CHARM = "identity-platform-login-ui-operator"
LOGIN_UI_APP = "login-ui"


async def get_unit_address(ops_test: OpsTest, app_name: str, unit_num: int) -> str:
    """Get private address of a unit."""
    status = await ops_test.model.get_status()  # noqa: F821
    return status["applications"][app_name]["units"][f"{app_name}/{unit_num}"]["address"]


@pytest.mark.abort_on_fail
async def test_build_and_deploy(ops_test: OpsTest):
    """Build the charm-under-test and deploy it together with related charms.

    Assert on the unit status before any relations/configurations take place.
    """
    # Build and deploy charm from local source folder
    charm = await ops_test.build_charm(".")
    resources = {"oci-image": METADATA["resources"]["oci-image"]["upstream-source"]}

    await ops_test.model.deploy(charm, resources=resources, application_name=APP_NAME)
    await ops_test.model.deploy(
        LOGIN_UI_CHARM,
        application_name=LOGIN_UI_APP,
        channel="latest/stable",
        trust=True,
        )
    await ops_test.model.integrate(APP_NAME, LOGIN_UI_APP)

    await ops_test.model.wait_for_idle(
        apps=[APP_NAME, LOGIN_UI_APP], status="active", timeout=1000,
    )


async def test_app_health(ops_test: OpsTest):
    public_address = await get_unit_address(ops_test, APP_NAME, 0)

    resp = requests.get(f"http://{public_address}:8080/api/v0/status")

    resp.raise_for_status()
