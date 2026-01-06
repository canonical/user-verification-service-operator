# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

import functools
import os
from pathlib import Path
from typing import AsyncGenerator, Callable, Optional

import httpx
import pytest
import pytest_asyncio
import yaml
import jubilant

from constants import INGRESS_INTEGRATION_NAME, LOGIN_UI_INTEGRATION_NAME

METADATA = yaml.safe_load(Path("./charmcraft.yaml").read_text())
APP_NAME = METADATA["name"]
TRAEFIK_CHARM = "traefik-k8s"
TRAEFIK_APP = "traefik"
INGRESS_DOMAIN = "public"
LOGIN_UI_CHARM = "identity-platform-login-ui-operator"
LOGIN_UI_APP = "login-ui"


async def get_unit_data(ops_test: OpsTest, unit_name: str) -> dict:
    show_unit_cmd = (f"show-unit {unit_name}").split()
    stdout = await model.juju(*show_unit_cmd)
    cmd_output = yaml.safe_load(stdout)
    return cmd_output[unit_name]


async def get_integration_data(
    model: jubilant.Juju, app_name: str, integration_name: str, unit_num: int = 0
) -> Optional[dict]:
    data = await get_unit_data(model, f"{app_name}/{unit_num}")
    return next(
        (
            integration
            for integration in data["relation-info"]
            if integration["endpoint"] == integration_name
        ),
        None,
    )


async def get_app_integration_data(
    model: jubilant.Juju,
    app_name: str,
    integration_name: str,
    unit_num: int = 0,
) -> Optional[dict]:
    data = await get_integration_data(model, app_name, integration_name, unit_num)
    return data["application-data"] if data else None



@pytest_asyncio.fixture
async def app_integration_data(integrator_model: jubilant.Juju) -> Callable:
    return functools.partial(get_app_integration_data, integrator_model)


@pytest_asyncio.fixture
async def leader_ingress_integration_data(app_integration_data: Callable) -> dict:
    data = await app_integration_data(APP_NAME, INGRESS_INTEGRATION_NAME)
    assert data
    return data


@pytest_asyncio.fixture
async def login_ui_endpoint_integration_data(app_integration_data: Callable) -> dict:
    data = await app_integration_data(APP_NAME, LOGIN_UI_INTEGRATION_NAME)
    assert data
    return data


@pytest_asyncio.fixture(scope="module")
async def local_charm() -> Path:
    # in GitHub CI, charms are built with charmcraftcache and uploaded to $CHARM_PATH
    charm = os.getenv("CHARM_PATH")
    if not charm:
        # Use jubilant's build_charm if available, else fallback
        import subprocess
        subprocess.run(["charmcraft", "pack"], check=True)
        charm = next(Path(".").glob("*.charm"))
    return Path(charm)


@pytest_asyncio.fixture
async def http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(verify=False) as client:
        yield client


@pytest.fixture
def support_email() -> str:
    return "support@email.com"


@pytest_asyncio.fixture
async def charm_config(ops_test: OpsTest, support_email: str) -> dict:
    return {
        "support_email": support_email,
        "salesforce_enabled": False,
    }
