# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

# Charm constants
WORKLOAD_CONTAINER = "user-verification-service"
WORKLOAD_SERVICE = "user-verification-service"
API_TOKEN_SECRET_KEY = "api-token"
API_TOKEN_SECRET_LABEL = "apitokensecret"
CONFIG_CONSUMER_KEY_SECRET_KEY = "consumer-key"
CONFIG_CONSUMER_SECRET_SECRET_KEY = "consumer-secret"

# Application constants
SERVICE_COMMAND = "user-verification-service serve"
PORT = 8080

# Integration constants
INGRESS_INTEGRATION_NAME = "ingress"
KRATOS_INTEGRATION_NAME = "kratos"
LOGIN_UI_INTEGRATION_NAME = "ui-endpoint-info"
PROMETHEUS_SCRAPE_INTEGRATION_NAME = "metrics-endpoint"
LOGGING_INTEGRATION_NAME = "logging"
GRAFANA_DASHBOARD_INTEGRATION_NAME = "grafana-dashboard"
TEMPO_TRACING_INTEGRATION_NAME = "tracing"
REGISTRATION_WEBHOOK_INTEGRATION_NAME = "kratos-registration-webhook"
REGISTRATION_UI_INTEGRATION_NAME = "registration-endpoint-info"
PROMETHEUS_SCRAPE_INTEGRATION_NAME = "metrics-endpoint"
LOGGING_RELATION_NAME = "logging"
GRAFANA_DASHBOARD_INTEGRATION_NAME = "grafana-dashboard"
TEMPO_TRACING_INTEGRATION_NAME = "tracing"
