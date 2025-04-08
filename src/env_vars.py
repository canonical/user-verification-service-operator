# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

from typing import Mapping, Protocol, TypeAlias, Union

from constants import PORT

EnvVars: TypeAlias = Mapping[str, Union[str, bool]]

DEFAULT_CONTAINER_ENV = {
    "OTEL_HTTP_ENDPOINT": "",
    "OTEL_GRPC_ENDPOINT": "",
    "TRACING_ENABLED": False,
    "LOG_LEVEL": "info",
    "PORT": str(PORT),
    "ERROR_UI_URL": "",
    "SUPPORT_EMAIL": "",
    "DIRECTORY_API_URL": "",
}


class EnvVarConvertible(Protocol):
    """An interface enforcing the contribution to workload service environment variables."""

    def to_env_vars(self) -> EnvVars:
        pass
