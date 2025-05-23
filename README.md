# Charmed User Verification Service for the Canonical Identity Platform

[![CharmHub Badge](https://charmhub.io/user-verification-service/badge.svg)](https://charmhub.io/user-verification-service)
[![Juju](https://img.shields.io/badge/Juju%20-3.0+-%23E95420)](https://github.com/juju/juju)
[![License](https://img.shields.io/github/license/canonical/user-verification-service-operator?label=License)](https://github.com/canonical/user-verification-service-operator/blob/main/LICENSE)

[![Continuous Integration Status](https://github.com/canonical/user-verification-service-operator/actions/workflows/on_push.yaml/badge.svg?branch=main)](https://github.com/canonical/user-verification-service-operator/actions?query=branch%3Amain)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196.svg)](https://conventionalcommits.org)

## Description

Python Operator for the Canonical Identity Platform User Verification Service

## Usage

Deploy the charms:

```shell
juju deploy user-verification-service --trust
juju deploy identity-platform --trust
```

You can follow the deployment status with `watch -c juju status --color`.

### Configuration

Now that we have deployed our charms, we will need to configure the charm.

First we need to create a juju secret with the consumer id/secret:

```console
juju add-secret salesforce-consumer consumer-key=<consumer_key> consumer-secret=<consumer_secret>
```

Now we need to grant access to the secret to the charm:

```console
juju grant-secret salesforce-consumer user-verification-service
```

Then you will have to configure the charm, eg:

```console
juju config user-verification-service \
  salesforce_domain=https://canonicalhr--staging.sandbox.my.salesforce.com \
  salesforce_consumer_secret=salesforce-consumer
```

Now you can integrate the charm with the identity-platform:

```console
juju integrate user-verification-service:kratos-registration-webhook kratos
juju integrate user-verification-service:registration-endpoint-info kratos
juju integrate user-verification-service identity-platform-login-ui
juju integrate user-verification-service traefik-public
```

Once the charms reach an active state, any users that try to log in to the identity-platform for the first time will be checked against the Salesforce API.

## Security

Please see [SECURITY.md](https://github.com/canonical/user-verification-service-operator/blob/main/SECURITY.md)
for guidelines on reporting security issues.

## Contributing

Please see the [Juju SDK docs](https://juju.is/docs/sdk) for guidelines on
enhancements to this charm following best practice guidelines,
and [CONTRIBUTING.md](https://github.com/canonical/user-verification-service-operator/blob/main/CONTRIBUTING.md)
for developer guidance.

## License

The Charmed User Verification Service is free software, distributed under the Apache
Software License, version 2.0.
See [LICENSE](https://github.com/canonical/user-verification-service-operator/blob/main/LICENSE)
for more information.
