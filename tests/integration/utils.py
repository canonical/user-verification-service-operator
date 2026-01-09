# Copyright 2026 Canonical Ltd.
# See LICENSE file for licensing details.

from contextlib import contextmanager
from typing import Iterator, Optional

import jubilant
import yaml
from tests.integration.constants import APP_NAME
from tenacity import retry, stop_after_attempt, wait_exponential

def juju_model_factory(model_name: str) -> jubilant.Juju:
    juju = jubilant.Juju()
    try:
        juju.add_model(model_name, config={"logging-config": "<root>=INFO"})
    except jubilant.CLIError as e:
        if "already exists" not in e.stderr:
            raise

        juju.model = model_name

    return juju

def get_unit_data(juju: jubilant.Juju, unit_name: str) -> dict:
    """Get the data for a given unit."""
    stdout = juju.cli("show-unit", unit_name)
    cmd_output = yaml.safe_load(stdout)
    return cmd_output[unit_name]


def get_integration_data(
    juju: jubilant.Juju, app_name: str, integration_name: str, unit_num: int = 0
) -> Optional[dict]:
    """Get the integration data for a given integration."""
    data = get_unit_data(juju, f"{app_name}/{unit_num}")
    return next(
        (
            integration
            for integration in data["relation-info"]
            if integration["endpoint"] == integration_name
        ),
        None,
    )


def get_app_integration_data(
    juju: jubilant.Juju,
    app_name: str,
    integration_name: str,
    unit_num: int = 0,
) -> Optional[dict]:
    """Get the application data for a given integration."""
    data = get_integration_data(juju, app_name, integration_name, unit_num)
    return data["application-data"] if data else None

def get_unit_address(juju: jubilant.Juju, app_name: str, unit_num: int = 0) -> str:
    """Get the address of a given unit."""
    data = get_unit_data(juju, f"{app_name}/{unit_num}")
    return data["address"]

# def unit_address(juju: jubilant.Juju, *, app_name: str, unit_num: int = 0) -> str:
#     """Get the address of a unit."""
#     status_yaml = juju.cli("status", "--format", "yaml")
#     status = yaml.safe_load(status_yaml)
#     return status["applications"][app_name]["units"][f"{app_name}/{unit_num}"]["address"]


def wait_for_active_idle(juju: jubilant.Juju, apps: list[str], timeout: float = 1000) -> None:
    """Wait for all applications and their units to be active and idle."""

    def condition(s: jubilant.Status) -> bool:
        return jubilant.all_active(s, *apps) and jubilant.all_agents_idle(s, *apps)

    juju.wait(condition, error=jubilant.any_error, timeout=timeout)


def wait_for_status(
    juju: jubilant.Juju, apps: list[str], status: str, timeout: float = 1000
) -> None:
    """Wait for all applications and their units to reach the given status."""

    def condition(s: jubilant.Status) -> bool:
        return all(s.apps[app_name].app_status.current == status for app_name in apps)

    juju.wait(condition, timeout=timeout)


@contextmanager
def remove_integration(
    juju: jubilant.Juju, /, remote_app_name: str, integration_name: str
) -> Iterator[None]:
    """Temporarily remove an integration from the application.

    Integration is restored after the context is exited.
    """

    # The pre-existing integration instance can still be "dying" when the `finally` block
    # is called, so `tenacity.retry` is used here to capture the `jubilant.CLIError`
    # and re-run `juju integrate ...` until the previous integration instance has finished dying.
    @retry(
        wait=wait_exponential(multiplier=2, min=1, max=30),
        stop=stop_after_attempt(10),
        reraise=True,
    )
    def _reintegrate() -> None:
        juju.integrate(f"{APP_NAME}:{integration_name}", remote_app_name)

    juju.remove_relation(f"{APP_NAME}:{integration_name}", remote_app_name)
    try:
        yield
    finally:
        _reintegrate()