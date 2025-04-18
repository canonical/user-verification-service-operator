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

```shell
juju deploy user-verification-service --trust
```

You can follow the deployment status with `watch -c juju status --color`.
