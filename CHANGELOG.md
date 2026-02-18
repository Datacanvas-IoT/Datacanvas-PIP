# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

-

### Changed

-

### Deprecated

-

### Removed

-

### Fixed

-

### Security

-

## [1.0.0] - 2026-02-18

### Added

- Initial public release published to PyPI as `v1.0.0`.

- SDK entrypoint: `DataCanvas` client exported from `datacanvas` package exposing `devices` and `data` resources and re-exporting types, constants, and errors.

- Device management resource: `DevicesResource` with `list()` method to retrieve project devices via the `/access-keys/external/devices` endpoint.

- Data retrieval resource: `DataResource` with `list(**kwargs)` providing filtering, pagination, and validation for datatable queries against `/access-keys/external/data`.

- Types & defaults: `SDKConfig`, `GetDataParams`, `Device`, `DataPoint`, `DataResponse`, and default configuration (pagination and limit defaults and caps) using frozen dataclasses.

- Comprehensive exception hierarchy: `DataCanvasError`, `AuthenticationError`, `AuthorizationError`, `ValidationError`, `NotFoundError`, `RateLimitError`, `ServerError`, `NetworkError`.

- Full type annotations with `py.typed` marker for static analysis support (mypy / pyright).

- Context manager support for automatic HTTP session cleanup.

- GitHub Actions CI/CD workflows for PyPI publishing and dry-run validation.

### Changed

-

### Fixed

-

This project follows the Keep a Changelog format and Semantic Versioning.

[unreleased]: https://github.com/Datacanvas-IoT/Datacanvas-PIP/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Datacanvas-IoT/Datacanvas-PIP/releases/tag/v1.0.0
