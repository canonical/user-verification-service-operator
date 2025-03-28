# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.

from unittest.mock import MagicMock, PropertyMock, create_autospec

import pytest
from ops import CollectStatusEvent, EventBase
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
def mocked_collect_status_event() -> MagicMock:
    return create_autospec(CollectStatusEvent)


@pytest.fixture
def all_satisfied_conditions(mocker: MockerFixture) -> None:
    mocker.patch("charm.container_connectivity", return_value=True)
