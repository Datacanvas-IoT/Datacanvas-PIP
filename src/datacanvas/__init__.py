"""
DataCanvas SDK for Python.

Official Python SDK for the DataCanvas IoT Platform.
A modern, type-safe, and resource-based client library for seamless
integration with the DataCanvas API.

Example:
    >>> from datacanvas import DataCanvas, SortOrder
    >>>
    >>> client = DataCanvas(
    ...     access_key_client="your-access-key-id",
    ...     access_key_secret="your-secret-key",
    ...     project_id=123,
    ... )
    >>>
    >>> devices = client.devices.list()
    >>> data = client.data.list(
    ...     table_name="temperature_sensors",
    ...     devices=[1, 2, 3],
    ...     limit=50,
    ...     order=SortOrder.DESC,
    ... )
"""

from datacanvas.client import DataCanvas
from datacanvas.types import SDKConfig, GetDataParams, DeviceResponse, Device, DataResponse, DataPoint
from datacanvas.core.constants import SortOrder, Endpoints, HttpMethod, DEFAULT_PAGE, DEFAULT_LIMIT, DEFAULT_ORDER, MAX_LIMIT
from datacanvas.core.exceptions import (
    DataCanvasError,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    NetworkError,
)

__version__ = "1.0.0"

__all__ = [
    # Main client
    "DataCanvas",
    # Types
    "SDKConfig",
    "GetDataParams",
    "DeviceResponse",
    "Device",
    "DataResponse",
    "DataPoint",
    # Constants
    "SortOrder",
    "Endpoints",
    "HttpMethod",
    "DEFAULT_PAGE",
    "DEFAULT_LIMIT",
    "DEFAULT_ORDER",
    "MAX_LIMIT",
    # Exceptions
    "DataCanvasError",
    "AuthenticationError",
    "AuthorizationError",
    "ValidationError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "NetworkError",
]
