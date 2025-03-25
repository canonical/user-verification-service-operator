/**
 * # Terraform Module for User Verification Service K8s Operator
 *
 * This is a Terraform module facilitating the deployment of the
 * user-verification-service charm using the Juju Terraform provider.
 */

resource "juju_application" "application" {
  name        = var.app_name
  model       = var.model_name
  trust       = true
  config      = var.config
  constraints = var.constraints
  units       = var.units

  charm {
    name     = "user-verification-service"
    base     = var.base
    channel  = var.channel
    revision = var.revision
  }
}
