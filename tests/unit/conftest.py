# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

from typing import Dict, List
from unittest.mock import MagicMock, PropertyMock, create_autospec

import pytest
from ops import CollectStatusEvent, EventBase, testing
from ops.model import Container, Unit
from pytest_mock import MockerFixture


@pytest.fixture
def mocked_workload_service_version(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "charm.WorkloadService.version", new_callable=PropertyMock, return_value="1.10.0"
    )


@pytest.fixture
def mocked_charm_holistic_handler(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("charm.UserVerificationServiceOperatorCharm._holistic_handler")


@pytest.fixture
def mocked_open_port(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("charm.WorkloadService.open_port")


@pytest.fixture
def mocked_container() -> MagicMock:
    return create_autospec(Container)


@pytest.fixture
def mocked_unit(mocked_container: MagicMock) -> MagicMock:
    mocked = create_autospec(Unit)
    mocked.get_container.return_value = mocked_container
    return mocked


@pytest.fixture
def mocked_event() -> MagicMock:
    return create_autospec(EventBase)


@pytest.fixture
def ingress_integration_data() -> dict:
    return {
        "external_host": "some-host",
        "scheme": "http",
    }


@pytest.fixture
def ingress_integration(ingress_integration_data: dict) -> testing.Relation:
    return testing.Relation(
        endpoint="ingress",
        interface="traefik_route",
        remote_app_name="traefik",
        remote_app_data=ingress_integration_data,
    )


@pytest.fixture
def login_ui_integration_data() -> dict:
    return {
        "consent_url": "http://login-ui.org/ui/consent",
        "error_url": "http://login-ui.org/ui/error",
        "login_url": "http://login-ui.org/ui/login",
        "oidc_error_url": "http://login-ui.org/ui/oidc_error",
        "device_verification_url": "http://login-ui.org/ui/device_verification",
        "post_device_done_url": "http://login-ui.org/ui/post_device_done",
        "recovery_url": "http://login-ui.org/ui/recovery",
        "settings_url": "http://login-ui.org/ui/settings",
        "webauthn_settings_url": "http://login-ui.org/ui/webauthn_settings",
    }


@pytest.fixture
def login_ui_integration(login_ui_integration_data: dict) -> testing.Relation:
    return testing.Relation(
        endpoint="ui-endpoint-info",
        interface="login_ui_endpoints",
        remote_app_name="login-ui",
        remote_app_data=login_ui_integration_data,
    )


@pytest.fixture()
def api_token() -> str:
    return "secret"


@pytest.fixture()
def salesforce_consumer_info() -> Dict[str, str]:
    return {"consumer-key": "key", "consumer-secret": "secret"}


@pytest.fixture()
def api_token_secret(api_token: str) -> testing.Secret:
    return testing.Secret(
        tracked_content={"api-token": api_token},
        label="apitokensecret",
    )


@pytest.fixture()
def salesforce_consumer_secret(salesforce_consumer_info: str) -> testing.Secret:
    return testing.Secret(
        tracked_content=salesforce_consumer_info,
    )


@pytest.fixture()
def mocked_secrets(
    api_token_secret: testing.Secret, salesforce_consumer_secret: testing.Secret
) -> List[testing.Secret]:
    return [api_token_secret, salesforce_consumer_secret]


@pytest.fixture
def support_email() -> str:
    return "support@email.com"


@pytest.fixture
def salesforce_domain() -> str:
    return "https://domain.salesforce.com"


@pytest.fixture
def charm_config(
    support_email: str, salesforce_domain: str, salesforce_consumer_secret: testing.Secret
) -> dict:
    return {
        "support_email": support_email,
        "directory_api_url": salesforce_domain,
        "directory_api_token": salesforce_consumer_secret.id,
    }


@pytest.fixture
def mocked_collect_status_event() -> MagicMock:
    return create_autospec(CollectStatusEvent)


@pytest.fixture
def all_satisfied_conditions(mocker: MockerFixture) -> None:
    mocker.patch("charm.container_connectivity", return_value=True)
    mocker.patch("charm.login_ui_integration_exists", return_value=True)
    mocker.patch("charm.Secrets.is_ready", return_value=True)
    mocker.patch("charm.CharmConfig.get_missing_config_keys", return_value=[])
