#!/usr/bin/env python3
# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

import http
import logging
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import requests
import jubilant

from tests.integration.constants import (
    APP_NAME,
    INGRESS_DOMAIN,
    LOGIN_UI_APP,
    LOGIN_UI_CHARM,
    METADATA,
    TRAEFIK_APP,
    TRAEFIK_CHARM,
)

logger = logging.getLogger(__name__)



def get_unit_address(model: jubilant.Juju, app_name: str, unit_num: int) -> str:
    """Get private address of a unit."""
    status = model.get_status()
    return status["applications"][app_name]["units"][f"{app_name}/{unit_num}"]["address"]



def test_build_and_deploy(
    model: jubilant.Juju,
    local_charm: Path,
    charm_config: dict,
) -> None:
    resources = {"oci-image": METADATA["resources"]["oci-image"]["upstream-source"]}
    model.deploy(
        local_charm,
        resources=resources,
        application_name=APP_NAME,
        config=charm_config,
    )
    model.deploy(
        TRAEFIK_CHARM,
        application_name=TRAEFIK_APP,
        channel="latest/stable",
        config={"external_hostname": INGRESS_DOMAIN},
        trust=True,
    )
    model.deploy(
        LOGIN_UI_CHARM,
        application_name=LOGIN_UI_APP,
        channel="latest/stable",
        trust=True,
    )
    model.integrate(TRAEFIK_APP, APP_NAME)
    model.integrate(APP_NAME, LOGIN_UI_APP)
    model.integrate(TRAEFIK_APP, LOGIN_UI_APP)
    model.wait(lambda status: jubilant.all_active(status, [LOGIN_UI_APP, TRAEFIK_APP, APP_NAME]))



def test_app_health(model: jubilant.Juju) -> None:
    public_address = get_unit_address(model, APP_NAME, 0)
    resp = requests.get(f"http://{public_address}:8080/api/v0/status")
    resp.raise_for_status()



def test_public_ingress_integration(
    model: jubilant.Juju
) -> None:
    address = get_unit_address(model, TRAEFIK_APP, 0)
    url = f"https://{address}/{model.model_name}-{APP_NAME}/ui/registration_error"
    resp = requests.get(url, allow_redirects=False, verify=False)
    assert resp.status_code == http.HTTPStatus.SEE_OTHER


def test_error_redirect(
    model: jubilant.Juju,
    login_ui_endpoint_integration_data: dict,
    support_email: str,
) -> None:
    address = get_unit_address(model, TRAEFIK_APP, 0)
    url = f"https://{address}/{model.model_name}-{APP_NAME}/ui/registration_error"
    resp = requests.get(url, allow_redirects=False, verify=False)
    assert resp.headers.get("location").startswith(
        login_ui_endpoint_integration_data["oidc_error_url"]
    )
    loc = urlparse(resp.headers.get("location"))
    q = parse_qs(loc.query)
    assert f"contact support at {support_email}" in q.get("error_description")[0]
