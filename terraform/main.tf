/**
 * # Terraform Module for User Verification Service K8s Operator
 *
 * This is a Terraform module facilitating the deployment of the
 * user-verification-service charm using the Juju Terraform provider.
 */

resource "juju_application" "application" {
  name  = var.app_name
  model = var.model_name
  trust = true
  config = merge(
    var.config,
    { salesforce_consumer_secret = format("secret:%s", var.salesforce_credentials_secret_id) }
  )
  constraints = var.constraints
  units       = var.units

  charm {
    name     = "user-verification-service"
    base     = var.base
    channel  = var.channel
    revision = var.revision
  }
}
