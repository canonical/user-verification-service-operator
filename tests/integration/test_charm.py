#!/usr/bin/env python3
# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

import asyncio
import http
import logging
from pathlib import Path
from urllib.parse import parse_qs, urlparse


import httpx
import pytest
import jubilant

from tests.integration.conftest import (
    APP_NAME,
    INGRESS_DOMAIN,
    LOGIN_UI_APP,
    LOGIN_UI_CHARM,
    METADATA,
    TRAEFIK_APP,
    TRAEFIK_CHARM,
)

logger = logging.getLogger(__name__)



async def get_unit_address(model: jubilant.Juju, app_name: str, unit_num: int) -> str:
    """Get private address of a unit."""
    status = await model.get_status()
    return status["applications"][app_name]["units"][f"{app_name}/{unit_num}"]["address"]



def test_build_and_deploy(
    integrator_model: jubilant.Juju,
    local_charm: Path,
    charm_config: dict,
) -> None:
    resources = {"oci-image": METADATA["resources"]["oci-image"]["upstream-source"]}
    integrator_model.deploy(
        local_charm,
        resources=resources,
        application_name=APP_NAME,
        config=charm_config,
    )
    integrator_model.deploy(
        TRAEFIK_CHARM,
        application_name=TRAEFIK_APP,
        channel="latest/stable",
        config={"external_hostname": INGRESS_DOMAIN},
        trust=True,
    )
    integrator_model.deploy(
        LOGIN_UI_CHARM,
        application_name=LOGIN_UI_APP,
        channel="latest/stable",
        trust=True,
    )
    integrator_model.integrate(TRAEFIK_APP, APP_NAME)
    integrator_model.integrate(APP_NAME, LOGIN_UI_APP)
    integrator_model.integrate(TRAEFIK_APP, LOGIN_UI_APP)
    integrator_model.wait(lambda status: jubilant.all_active(status, [LOGIN_UI_APP, TRAEFIK_APP, APP_NAME]))



async def test_app_health(integrator_model: jubilant.Juju, http_client: httpx.AsyncClient) -> None:
    public_address = await get_unit_address(integrator_model, APP_NAME, 0)
    resp = await http_client.get(f"http://{public_address}:8080/api/v0/status")
    resp.raise_for_status()



async def test_public_ingress_integration(
    integrator_model: jubilant.Juju, http_client: httpx.AsyncClient
) -> None:
    address = await get_unit_address(integrator_model, TRAEFIK_APP, 0)
    url = f"https://{address}/{integrator_model.model_name}-{APP_NAME}/ui/registration_error"
    resp = await http_client.get(url, follow_redirects=False)
    assert resp.status_code == http.HTTPStatus.SEE_OTHER



async def test_error_redirect(
    integrator_model: jubilant.Juju,
    login_ui_endpoint_integration_data: dict,
    http_client: httpx.AsyncClient,
    support_email: str,
) -> None:
    address = await get_unit_address(integrator_model, TRAEFIK_APP, 0)
    url = f"https://{address}/{integrator_model.model_name}-{APP_NAME}/ui/registration_error"
    resp = await http_client.get(url, follow_redirects=False)
    assert resp.headers.get("location").startswith(
        login_ui_endpoint_integration_data["oidc_error_url"]
    )
    loc = urlparse(resp.headers.get("location"))
    q = parse_qs(loc.query)
    assert f"contact support at {support_email}" in q.get("error_description")[0]
