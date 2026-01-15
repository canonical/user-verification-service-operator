# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

import functools
import os
import uuid
from collections.abc import Generator
from contextlib import suppress
from pathlib import Path
from typing import Callable, Iterator

import jubilant
import pytest
import requests

from src.constants import INGRESS_INTEGRATION_NAME, LOGIN_UI_INTEGRATION_NAME
from tests.integration.constants import APP_NAME
from tests.integration.utils import (
    get_app_integration_data,
    juju_model_factory,
)


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add custom command-line options for model management and deployment control.

    This function adds the following options:
        --keep-models: Keep the Juju model after the test is finished.
        --model: Specify the Juju model to run the tests on.
        --no-deploy: Skip deployment of the charm.
    """
    parser.addoption(
        "--keep-models",
        "--no-teardown",
        action="store_true",
        default=False,
        help="Keep the model after the test is finished.",
    )
    parser.addoption(
        "--model",
        action="store",
        default=None,
        help="The model to run the tests on.",
    )
    parser.addoption(
        "--no-deploy",
        action="store_true",
        default=False,
        help="Skip deployment of the charm.",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers for test selection based on deployment and model management.

    This function registers the following markers:
        skip_if_deployed: Skip tests if the charm is already deployed.
        skip_if_keep_models: Skip tests if the --keep-models option is set.
    """
    config.addinivalue_line("markers", "skip_if_deployed: skip test if deployed")
    config.addinivalue_line("markers", "skip_if_keep_models: skip test if --keep-models is set.")


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Modify collected test items based on command-line options.

    This function skips tests with specific markers based on the provided command-line options:
        - If --no-deploy is set, tests marked with "skip_if_deployed
          are skipped.
        - If --keep-models is set, tests marked with "skip_if_keep_models"
          are skipped.
    """
    for item in items:
        if config.getoption("--no-deploy") and "skip_if_deployed" in item.keywords:
            skip_deployed = pytest.mark.skip(reason="skipping deployment")
            item.add_marker(skip_deployed)
        if config.getoption("--keep-models") and "skip_if_keep_models" in item.keywords:
            skip_keep_models = pytest.mark.skip(
                reason="skipping test because --keep-models is set"
            )
            item.add_marker(skip_keep_models)


@pytest.fixture(scope="session")
def juju(request: pytest.FixtureRequest) -> Iterator[jubilant.Juju]:
    if not hasattr(request.session, "juju_model_name"):
        model_name = request.config.getoption("--model")
        if not model_name:
            model_name = f"test-user-verification-{uuid.uuid4().hex[-8:]}"
        setattr(request.session, "juju_model_name", model_name)

    juju_ = juju_model_factory(getattr(request.session, "juju_model_name"))
    juju_.wait_timeout = 10 * 60

    yield juju_

    if request.session.testsfailed:
        log = juju_.debug_log(limit=1000)
        print(log, end="")

    no_teardown = bool(request.config.getoption("--no-teardown"))
    keep_model = no_teardown or request.session.testsfailed > 0
    if not keep_model:
        with suppress(jubilant.CLIError):
            args = [
                "destroy-model",
                getattr(request.session, "juju_model_name"),
                "--no-prompt",
                "--destroy-storage",
                "--force",
                "--timeout",
                "600s",
            ]
            juju_.cli(*args, include_model=False)


@pytest.fixture
def app_integration_data(juju: jubilant.Juju) -> Callable:
    return functools.partial(get_app_integration_data, juju)


@pytest.fixture
def leader_ingress_integration_data(app_integration_data: Callable) -> dict:
    data = app_integration_data(APP_NAME, INGRESS_INTEGRATION_NAME)
    assert data
    return data


@pytest.fixture
def login_ui_endpoint_integration_data(app_integration_data: Callable) -> dict:
    data = app_integration_data(APP_NAME, LOGIN_UI_INTEGRATION_NAME)
    assert data
    return data


@pytest.fixture(scope="module")
def local_charm() -> Path:
    # in GitHub CI, charms are built with charmcraftcache and uploaded to $CHARM_PATH
    charm = os.getenv("CHARM_PATH")
    if not charm:
        # Use jubilant's build_charm if available, else fallback
        import subprocess

        subprocess.run(["charmcraft", "pack"], check=True)
        charm = next(Path(".").glob("*.charm"))
    return Path(charm)


@pytest.fixture
def support_email() -> str:
    return "support@email.com"


@pytest.fixture
def charm_config(support_email: str) -> dict:
    return {
        "support_email": support_email,
        "salesforce_enabled": False,
    }


@pytest.fixture
def http_client() -> Generator[requests.Session, None, None]:
    with requests.Session() as client:
        client.verify = False
        yield client
