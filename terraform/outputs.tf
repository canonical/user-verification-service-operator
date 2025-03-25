# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

output "app_name" {
  description = "The Juju application name"
  value       = juju_application.application.name
}

output "requires" {
  description = "The Juju integrations that the charm requires"
  value = {
    ui-endpoint-info = "ui-endpoint-info"
    ingress          = "ingress"
    logging          = "logging"
    tracing          = "tracing"
  }
}

output "provides" {
  description = "The Juju integrations that the charm provides"
  value = {
    kratos-registration-webhook = "kratos-registration-webhook"
    registration-endpoint-info  = "registration-endpoint-info"
    metrics-endpoint            = "metrics-endpoint"
    grafana-dashboard           = "grafana-dashboard"
  }
}
