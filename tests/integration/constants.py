# Copyright 2026 Canonical Ltd.
# See LICENSE file for licensing details.

from pathlib import Path
import yaml

METADATA = yaml.safe_load(Path("./charmcraft.yaml").read_text())
APP_NAME = METADATA["name"]
TRAEFIK_CHARM = "traefik-k8s"
TRAEFIK_APP = "traefik"
INGRESS_DOMAIN = "public"
LOGIN_UI_CHARM = "identity-platform-login-ui-operator"
LOGIN_UI_APP = "login-ui"