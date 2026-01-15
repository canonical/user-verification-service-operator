#!/usr/bin/env python3
# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

import http
import logging
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import jubilant
import pytest
import requests

from tests.integration.constants import (
    APP_NAME,
    INGRESS_DOMAIN,
    LOCAL_CHARM,
    LOGIN_UI_APP,
    LOGIN_UI_CHARM,
    METADATA,
    TRAEFIK_APP,
    TRAEFIK_CHARM,
)
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
    juju.deploy(
        TRAEFIK_CHARM,
        app=TRAEFIK_APP,
        channel="latest/stable",
        config={"external_hostname": INGRESS_DOMAIN},
        trust=True,
    )
    juju.deploy(
        LOGIN_UI_CHARM,
        app=LOGIN_UI_APP,
        channel="latest/stable",
        trust=True,
    )
    juju.integrate(TRAEFIK_APP, APP_NAME)
    juju.integrate(APP_NAME, LOGIN_UI_APP)
    juju.integrate(TRAEFIK_APP, LOGIN_UI_APP)
    juju.wait(
        ready=all_active(
            LOGIN_UI_APP,
            TRAEFIK_APP,
            APP_NAME,
        ),
        error=any_error(
            LOGIN_UI_APP,
            TRAEFIK_APP,
            APP_NAME,
        ),
        timeout=10 * 60,
    )


def test_app_health(juju: jubilant.Juju, http_client: requests.Session) -> None:
    public_address = get_unit_address(juju, APP_NAME, 0)
    resp = http_client.get(f"http://{public_address}:8080/api/v0/status")
    resp.raise_for_status()


def test_public_ingress_integration(request: pytest.FixtureRequest, juju: jubilant.Juju) -> None:
    address = get_unit_address(juju, TRAEFIK_APP, 0)
    model_name = getattr(request.session, "juju_model_name")
    url = f"https://{address}/{model_name}-{APP_NAME}/ui/registration_error"
    resp = requests.get(url, allow_redirects=False, verify=False)
    assert resp.status_code == http.HTTPStatus.SEE_OTHER


def test_error_redirect(
    request: pytest.FixtureRequest,
    juju: jubilant.Juju,
    login_ui_endpoint_integration_data: dict,
    support_email: str,
) -> None:
    address = get_unit_address(juju, TRAEFIK_APP, 0)
    model_name = getattr(request.session, "juju_model_name")

    url = f"https://{address}/{model_name}-{APP_NAME}/ui/registration_error"
    resp = requests.get(url, allow_redirects=False, verify=False)
    assert resp.headers.get("location").startswith(
        login_ui_endpoint_integration_data["oidc_error_url"]
    )
    loc = urlparse(resp.headers.get("location"))
    q = parse_qs(loc.query)
    assert f"contact support at {support_email}" in q.get("error_description")[0]
