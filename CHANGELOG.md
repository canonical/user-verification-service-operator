# Changelog

## [1.3.4](https://github.com/canonical/user-verification-service-operator/compare/v1.3.3...v1.3.4) (2025-11-12)


### Bug Fixes

* change lib name ([016b9dd](https://github.com/canonical/user-verification-service-operator/commit/016b9dd0d00e87d1c6d39b2afe07946b2eef73e8))
* check service status before setting status ([7f7d364](https://github.com/canonical/user-verification-service-operator/commit/7f7d3640c73e82b17a908f92f34d5c6d6172cde0))
* check service status before setting status ([530ab8c](https://github.com/canonical/user-verification-service-operator/commit/530ab8cba8db02aaf7927f2af0ff79112abc3f00))
* don't restart service if config didn't change ([b2dc340](https://github.com/canonical/user-verification-service-operator/commit/b2dc340fb9cbcce41e9288be192d698565f5a73e))
* update charm dependent libs ([60e5a6b](https://github.com/canonical/user-verification-service-operator/commit/60e5a6b9f676669056d480d0f9aceea32483238c))

## [1.3.3](https://github.com/canonical/user-verification-service-operator/compare/v1.3.2...v1.3.3) (2025-07-01)


### Bug Fixes

* bump kratos lib ([b0f83f5](https://github.com/canonical/user-verification-service-operator/commit/b0f83f58173da1731324fcbbf6dd4114033d528d))

## [1.3.2](https://github.com/canonical/user-verification-service-operator/compare/v1.3.1...v1.3.2) (2025-06-12)


### Bug Fixes

* add constraint refault value ([e140d1f](https://github.com/canonical/user-verification-service-operator/commit/e140d1f53948670947eda242f5c6f75e5428c914))

## [1.3.1](https://github.com/canonical/user-verification-service-operator/compare/v1.3.0...v1.3.1) (2025-06-12)


### Bug Fixes

* fix ci deploy wf ([2eb0cdc](https://github.com/canonical/user-verification-service-operator/commit/2eb0cdcc5c9e6b0a0e1d70979812e48837af7531))

## [1.3.0](https://github.com/canonical/user-verification-service-operator/compare/v1.2.0...v1.3.0) (2025-06-12)


### Features

* add terraform module ([c0c8f8b](https://github.com/canonical/user-verification-service-operator/commit/c0c8f8bbf68484117d249f68ca1c5a960a6ad1ae))
* add terraform module ([21c2078](https://github.com/canonical/user-verification-service-operator/commit/21c20786c6b8d8d2b9f8515dffba627706863e8b))
* use Salesforce instead of directory API ([bf1a035](https://github.com/canonical/user-verification-service-operator/commit/bf1a035770cc5ac8928b2273923782689f315475))


### Bug Fixes

* add API auth ([295ad1f](https://github.com/canonical/user-verification-service-operator/commit/295ad1fcb342b6d4fe4e5964115d01b2985ad9e0))
* add cos integration ([ab9c2f5](https://github.com/canonical/user-verification-service-operator/commit/ab9c2f5e529f0dc37a7f58752376fc1c384a65dd))
* add directory API configs ([826767c](https://github.com/canonical/user-verification-service-operator/commit/826767c67cf1fdf47a90d67cd01cc6cc06cef4e0))
* add http_proxy config ([6e2a3b0](https://github.com/canonical/user-verification-service-operator/commit/6e2a3b080079475200df7e269ff7a0e9ba4bf25c))
* add ingress integration ([fbcf726](https://github.com/canonical/user-verification-service-operator/commit/fbcf726ecd8cbf97b5a751d875cfb65779140c0a))
* add integration with the login UI ([59c60b2](https://github.com/canonical/user-verification-service-operator/commit/59c60b241d77ac3197366647563496ff913e53ad))
* add kratos integration ([9630571](https://github.com/canonical/user-verification-service-operator/commit/9630571432736d71be670f506c4374077b8fdff6))
* add resource constraints ([38febe2](https://github.com/canonical/user-verification-service-operator/commit/38febe2e6f4654ab2d93e2e9f1b89d3d47cbbbd7))
* add rust to build ([a521292](https://github.com/canonical/user-verification-service-operator/commit/a52129298709889c63587a394e3708d70bdc8db5))
* add support_email config ([15af776](https://github.com/canonical/user-verification-service-operator/commit/15af77623124ecf405a3815050f549835ef20417))
* add UI_BASE_URL ([9a1facd](https://github.com/canonical/user-verification-service-operator/commit/9a1facd655396e793123ce2e92cd879248fa77cb))
* add workload management logic ([7c39ff5](https://github.com/canonical/user-verification-service-operator/commit/7c39ff5028083156889e6f18f421ba78478e2f3f))
* address setupttols CVEs ([ce0287c](https://github.com/canonical/user-verification-service-operator/commit/ce0287c131396426c2bb0f515d1d4c5ee302fb0b)), closes [#31](https://github.com/canonical/user-verification-service-operator/issues/31)
* do not stop tests on traefik error ([07a4fad](https://github.com/canonical/user-verification-service-operator/commit/07a4fad5129442bcda66a06f77da99cd16be5038))
* fix tracing integration ([989c0d1](https://github.com/canonical/user-verification-service-operator/commit/989c0d1d43195f92536d29f5a40a97f3cf00e35e))
* run as non root ([e4efa3f](https://github.com/canonical/user-verification-service-operator/commit/e4efa3f1f092455262c343e17b667ea3318ce60c))
* set parse to False ([684ffa7](https://github.com/canonical/user-verification-service-operator/commit/684ffa7968208cdc01e5795aa4af7fb7fece8eac))
* set parse to True ([b48ffe4](https://github.com/canonical/user-verification-service-operator/commit/b48ffe48f2078d1b8910d7594b0368e507ab0c0f))
* update kratos_registration_web_hook lib ([7a50417](https://github.com/canonical/user-verification-service-operator/commit/7a504172d4356bbaf9a66490bc6ceb54529babc1))
* use traefik from stable ([83f03c2](https://github.com/canonical/user-verification-service-operator/commit/83f03c2ebf9e8a08e35426cb6dc4984a8499465e))

## [1.2.0](https://github.com/canonical/user-verification-service-operator/compare/v1.1.1...v1.2.0) (2025-05-30)


### Features

* use Salesforce instead of directory API ([bf1a035](https://github.com/canonical/user-verification-service-operator/commit/bf1a035770cc5ac8928b2273923782689f315475))


### Bug Fixes

* add resource constraints ([38febe2](https://github.com/canonical/user-verification-service-operator/commit/38febe2e6f4654ab2d93e2e9f1b89d3d47cbbbd7))
* run as non root ([e4efa3f](https://github.com/canonical/user-verification-service-operator/commit/e4efa3f1f092455262c343e17b667ea3318ce60c))
* set parse to True ([b48ffe4](https://github.com/canonical/user-verification-service-operator/commit/b48ffe48f2078d1b8910d7594b0368e507ab0c0f))

## [1.1.1](https://github.com/canonical/user-verification-service-operator/compare/v1.1.0...v1.1.1) (2025-05-06)


### Bug Fixes

* set parse to False ([684ffa7](https://github.com/canonical/user-verification-service-operator/commit/684ffa7968208cdc01e5795aa4af7fb7fece8eac))

## [1.1.0](https://github.com/canonical/user-verification-service-operator/compare/v1.0.1...v1.1.0) (2025-05-05)


### Features

* add terraform module ([c0c8f8b](https://github.com/canonical/user-verification-service-operator/commit/c0c8f8bbf68484117d249f68ca1c5a960a6ad1ae))
* add terraform module ([21c2078](https://github.com/canonical/user-verification-service-operator/commit/21c20786c6b8d8d2b9f8515dffba627706863e8b))


### Bug Fixes

* add API auth ([295ad1f](https://github.com/canonical/user-verification-service-operator/commit/295ad1fcb342b6d4fe4e5964115d01b2985ad9e0))
* add cos integration ([ab9c2f5](https://github.com/canonical/user-verification-service-operator/commit/ab9c2f5e529f0dc37a7f58752376fc1c384a65dd))
* add directory API configs ([826767c](https://github.com/canonical/user-verification-service-operator/commit/826767c67cf1fdf47a90d67cd01cc6cc06cef4e0))
* add ingress integration ([fbcf726](https://github.com/canonical/user-verification-service-operator/commit/fbcf726ecd8cbf97b5a751d875cfb65779140c0a))
* add integration with the login UI ([59c60b2](https://github.com/canonical/user-verification-service-operator/commit/59c60b241d77ac3197366647563496ff913e53ad))
* add kratos integration ([9630571](https://github.com/canonical/user-verification-service-operator/commit/9630571432736d71be670f506c4374077b8fdff6))
* add rust to build ([a521292](https://github.com/canonical/user-verification-service-operator/commit/a52129298709889c63587a394e3708d70bdc8db5))
* add support_email config ([15af776](https://github.com/canonical/user-verification-service-operator/commit/15af77623124ecf405a3815050f549835ef20417))
* add UI_BASE_URL ([9a1facd](https://github.com/canonical/user-verification-service-operator/commit/9a1facd655396e793123ce2e92cd879248fa77cb))
* add workload management logic ([7c39ff5](https://github.com/canonical/user-verification-service-operator/commit/7c39ff5028083156889e6f18f421ba78478e2f3f))
* address setupttols CVEs ([ce0287c](https://github.com/canonical/user-verification-service-operator/commit/ce0287c131396426c2bb0f515d1d4c5ee302fb0b)), closes [#31](https://github.com/canonical/user-verification-service-operator/issues/31)
* do not stop tests on traefik error ([07a4fad](https://github.com/canonical/user-verification-service-operator/commit/07a4fad5129442bcda66a06f77da99cd16be5038))
* fix tracing integration ([989c0d1](https://github.com/canonical/user-verification-service-operator/commit/989c0d1d43195f92536d29f5a40a97f3cf00e35e))
* update kratos_registration_web_hook lib ([7a50417](https://github.com/canonical/user-verification-service-operator/commit/7a504172d4356bbaf9a66490bc6ceb54529babc1))
* use traefik from stable ([83f03c2](https://github.com/canonical/user-verification-service-operator/commit/83f03c2ebf9e8a08e35426cb6dc4984a8499465e))

## [1.0.1](https://github.com/canonical/user-verification-service-operator/compare/v1.0.0...v1.0.1) (2025-04-22)


### Bug Fixes

* address setupttols CVEs ([ce0287c](https://github.com/canonical/user-verification-service-operator/commit/ce0287c131396426c2bb0f515d1d4c5ee302fb0b)), closes [#31](https://github.com/canonical/user-verification-service-operator/issues/31)

## 1.0.0 (2025-04-15)


### Bug Fixes

* add API auth ([295ad1f](https://github.com/canonical/user-verification-service-operator/commit/295ad1fcb342b6d4fe4e5964115d01b2985ad9e0))
* add cos integration ([ab9c2f5](https://github.com/canonical/user-verification-service-operator/commit/ab9c2f5e529f0dc37a7f58752376fc1c384a65dd))
* add ingress integration ([fbcf726](https://github.com/canonical/user-verification-service-operator/commit/fbcf726ecd8cbf97b5a751d875cfb65779140c0a))
* add integration with the login UI ([59c60b2](https://github.com/canonical/user-verification-service-operator/commit/59c60b241d77ac3197366647563496ff913e53ad))
* add kratos integration ([9630571](https://github.com/canonical/user-verification-service-operator/commit/9630571432736d71be670f506c4374077b8fdff6))
* add rust to build ([a521292](https://github.com/canonical/user-verification-service-operator/commit/a52129298709889c63587a394e3708d70bdc8db5))
* add support_email config ([15af776](https://github.com/canonical/user-verification-service-operator/commit/15af77623124ecf405a3815050f549835ef20417))
* add workload management logic ([7c39ff5](https://github.com/canonical/user-verification-service-operator/commit/7c39ff5028083156889e6f18f421ba78478e2f3f))
* do not stop tests on traefik error ([07a4fad](https://github.com/canonical/user-verification-service-operator/commit/07a4fad5129442bcda66a06f77da99cd16be5038))
* fix tracing integration ([989c0d1](https://github.com/canonical/user-verification-service-operator/commit/989c0d1d43195f92536d29f5a40a97f3cf00e35e))
* use traefik from stable ([83f03c2](https://github.com/canonical/user-verification-service-operator/commit/83f03c2ebf9e8a08e35426cb6dc4984a8499465e))
