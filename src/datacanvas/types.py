"""
Type definitions for the DataCanvas SDK.

Uses :mod:`dataclasses` for structured data and :class:`typing.TypedDict`
where appropriate.  All types are fully annotated for static analysis with
mypy / pyright.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from datacanvas.core.constants import SortOrder

__all__ = [
    "SDKConfig",
    "GetDataParams",
    "DeviceResponse",
    "Device",
    "DataResponse",
    "DataPoint",
]


@dataclass(frozen=True)
class SDKConfig:
    """Configuration options for initialising the DataCanvas SDK.

    All credentials should be obtained from the DataCanvas dashboard.

    Attributes:
        access_key_client: Client access key ID for API authentication.
        access_key_secret: Secret access key for API authentication.
        project_id: Project ID to scope API requests.
        base_url: Base URL for the DataCanvas API.
    """

    access_key_client: str
    access_key_secret: str
    project_id: int
    base_url: str


@dataclass(frozen=True)
class GetDataParams:
    """Parameters for retrieving data from a datatable.

    Only *table_name* is required; other parameters have sensible defaults.

    Attributes:
        table_name: Name of the datatable to query (required).
        devices: Optional list of device IDs to filter results.
        page: Page number for pagination (0-indexed, default: 0).
        limit: Number of items per page (default: 20, max: 1000).
        order: Sort order for results (default: ``SortOrder.DESC``).
    """

    table_name: str
    devices: Optional[List[int]] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    order: Optional[SortOrder] = None


@dataclass(frozen=True)
class Device:
    """Represents an IoT device in the DataCanvas platform.

    Attributes:
        device_id: Unique identifier for the device.
        device_name: Human-readable name for the device.
    """

    device_id: int
    device_name: str


@dataclass(frozen=True)
class DeviceResponse:
    """Response structure for device listing operations.

    Attributes:
        success: Indicates if the request was successful.
        devices: List of devices associated with the project.
    """

    success: bool
    devices: List[Device] = field(default_factory=list)


@dataclass(frozen=True)
class DataPoint:
    """Represents a single data point from a device.

    Contains standard fields plus dynamic fields based on the datatable schema.

    Attributes:
        id: Unique identifier for the data point.
        device: Device ID that generated this data point.
        extra: Additional dynamic fields from the datatable. Field names and
            types depend on the datatable schema.
    """

    id: int
    device: int
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DataResponse:
    """Response structure for data retrieval operations.

    Attributes:
        count: Total number of records matching the query.
        data: Data organised by device ID.  Each key is a device ID (as
            string), and the value is a list of data points.
    """

    count: int
    data: Dict[str, List[DataPoint]] = field(default_factory=dict)
