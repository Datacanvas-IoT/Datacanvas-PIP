# DataCanvas SDK for Python

[![PyPI version](https://img.shields.io/pypi/v/datacanvas.svg)](https://pypi.org/project/datacanvas/)
[![Python](https://img.shields.io/pypi/pyversions/datacanvas.svg)](https://pypi.org/project/datacanvas/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

Official Python SDK for the **DataCanvas IoT Platform**. A modern, type-safe, and resource-based client library for seamless integration with the DataCanvas API.

##  Features

-  **Resource-Based Architecture** — Intuitive API organised by domain concepts
-  **Type-Safe** — Full type annotations and `py.typed` marker for static analysis
-  **Modern** — Supports Python 3.9+, dataclasses, and enums
-  **Robust Error Handling** — Comprehensive error hierarchy for precise error management
-  **Minimal Dependencies** — Uses `requests` for HTTP; no unnecessary extras

##  Installation

```bash
pip install datacanvas
```

##  Quick Start

```python
import os
from datacanvas import DataCanvas, SortOrder

# Initialise SDK
client = DataCanvas(
    access_key_client=os.environ["DATACANVAS_ACCESS_KEY_ID"],
    access_key_secret=os.environ["DATACANVAS_SECRET_KEY"],
    project_id=int(os.environ["DATACANVAS_PROJECT_ID"]),
    base_url=os.environ["DATACANVAS_BASE_URL"],
)

# List all devices
devices = client.devices.list()
print(f"Found {len(devices.devices)} devices")

# Retrieve data from a datatable
data = client.data.list(
    table_name="temperature_sensors",
    devices=[1, 2, 3],
    page=0,
    limit=50,
    order=SortOrder.DESC,
)
print(f"Retrieved {data.count} data points")
```

### Context Manager

The SDK supports context managers for automatic resource cleanup:

```python
with DataCanvas(
    access_key_client="your-key",
    access_key_secret="your-secret",
    project_id=123,
    base_url="https://api.<something>.<something>",
) as client:
    devices = client.devices.list()
```

##  API Reference

### Configuration

#### `DataCanvas(**kwargs)`

Creates a new SDK instance.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `access_key_client` | `str` | ✅ | Client access key ID from DataCanvas dashboard |
| `access_key_secret` | `str` | ✅ | Secret access key for authentication |
| `project_id` | `int` | ✅ | Project ID to scope API requests |
| `base_url` | `str` | ✅ | Base URL for the DataCanvas API |

```python
client = DataCanvas(
    access_key_client="your-access-key-id",
    access_key_secret="your-secret-key",
    project_id=123,
    base_url="https://api.<something>.<something>",
)
```

---

### Device Management

#### `client.devices.list() -> DeviceResponse`

Retrieves all devices associated with the configured project.

```python
response = client.devices.list()

for device in response.devices:
    print(f"Device: {device.device_name} (ID: {device.device_id})")
```

**Response types:**

```python
@dataclass
class DeviceResponse:
    success: bool
    devices: list[Device]

@dataclass
class Device:
    device_id: int
    device_name: str
```

---

### Data Retrieval

#### `client.data.list(**kwargs) -> DataResponse`

Retrieves data from a specified datatable with optional filtering and pagination.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `table_name` | `str` | ✅ | — | Name of the datatable to query |
| `devices` | `list[int]` | ❌ | `[]` | List of device IDs to filter |
| `page` | `int` | ❌ | `0` | Page number (0-indexed) |
| `limit` | `int` | ❌ | `20` | Items per page (max: 1000) |
| `order` | `SortOrder` | ❌ | `DESC` | Sort order (ASC or DESC) |

```python
from datacanvas import SortOrder

# Retrieve all data
all_data = client.data.list(table_name="temperature_sensors")

# Retrieve with filtering and pagination
filtered = client.data.list(
    table_name="temperature_sensors",
    devices=[1, 2, 3],
    page=0,
    limit=50,
    order=SortOrder.DESC,
)

print(f"Total records: {filtered.count}")

for device_id, points in filtered.data.items():
    print(f"Device {device_id}: {len(points)} data points")
    for point in points:
        print(f"  - ID: {point.id}, Device: {point.device}, Extra: {point.extra}")
```

**Response types:**

```python
@dataclass
class DataResponse:
    count: int
    data: dict[str, list[DataPoint]]

@dataclass
class DataPoint:
    id: int
    device: int
    extra: dict[str, Any]  # Dynamic fields from datatable schema
```

---

##  Error Handling

The SDK provides comprehensive error handling with specific error types for different scenarios. All errors inherit from `DataCanvasError`.

### Error Types

| Error Class | Description | HTTP Status |
|-------------|-------------|-------------|
| `AuthenticationError` | Invalid credentials | 401 |
| `AuthorizationError` | Insufficient permissions | 403 |
| `ValidationError` | Invalid request parameters | 400, 422 |
| `NotFoundError` | Resource not found | 404 |
| `RateLimitError` | Rate limit exceeded | 429 |
| `ServerError` | Server-side error | 500+ |
| `NetworkError` | Network connectivity issue | — |

### Handling Errors

```python
from datacanvas import (
    DataCanvas,
    AuthenticationError,
    ValidationError,
    RateLimitError,
    NetworkError,
    DataCanvasError,
)

try:
    data = client.data.list(table_name="sensors", limit=100)
except AuthenticationError:
    print("Authentication failed. Check your credentials.")
except ValidationError as e:
    print(f"Invalid request: {e}")
except RateLimitError:
    print("Rate limit exceeded. Please wait.")
except NetworkError as e:
    print(f"Network error: {e}")
except DataCanvasError as e:
    print(f"SDK error: {e}")
```

---

##  Architecture

The SDK follows a **resource-based OOP architecture** with clear separation of concerns:

```
DataCanvas SDK
├── DataCanvas (Main Client)
│   ├── devices (DevicesResource)
│   └── data (DataResource)
├── HttpClient (HTTP Communication)
├── Exceptions (Error Hierarchy)
├── Constants (Enums & Defaults)
└── Types (Dataclass Definitions)
```

---

##  Python Type Checking

The SDK ships with a `py.typed` marker and full type annotations. Use with mypy or pyright:

```python
from datacanvas import DataCanvas, SDKConfig, DeviceResponse, DataResponse, DataPoint, GetDataParams
```

---

##  Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone repository
git clone https://github.com/Datacanvas-IoT/Datacanvas-PIP
cd Datacanvas-PIP

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run type checks
mypy src/datacanvas

# Run linter
ruff check src/
```

---

## License

This project is licensed under the **Apache License 2.0** — see the [LICENSE](LICENSE) file for details.

---

##  Resources

- [DataCanvas Platform](http://datacanvas.hypercube.lk/)
- [Issue Tracker](https://github.com/Datacanvas-IoT/Datacanvas-PIP/issues)
- [Changelog](CHANGELOG.md)

---

##  Support

For questions, issues, or feature requests:

- 📧 Email: datacanvasmgmt[at]gmail[dot]com
- 🐛 Issues: [GitHub Issues](https://github.com/Datacanvas-IoT/Datacanvas-PIP/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/Datacanvas-IoT/Datacanvas-PIP/discussions)

---

<p align="center">
  Made with ❤️ by the DataCanvas Team
</p>
