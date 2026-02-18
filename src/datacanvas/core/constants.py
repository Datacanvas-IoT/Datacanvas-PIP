"""
API endpoint paths, HTTP methods, sort orders, and default configuration
values used by the DataCanvas SDK.

Centralised constant management for maintainability.
"""

from enum import Enum

__all__ = [
    "Endpoints",
    "HttpMethod",
    "SortOrder",
    "DEFAULT_PAGE",
    "DEFAULT_LIMIT",
    "DEFAULT_ORDER",
    "MAX_LIMIT",
]


class Endpoints(str, Enum):
    """API endpoint paths used by the DataCanvas SDK."""

    DEVICES = "/access-keys/external/devices"
    """Endpoint for device management operations."""

    DATA = "/access-keys/external/data"
    """Endpoint for data retrieval operations."""


class HttpMethod(str, Enum):
    """Supported HTTP methods for API requests."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class SortOrder(str, Enum):
    """Sort order options for data queries.

    Attributes:
        ASC: Ascending order (oldest to newest, A-Z).
        DESC: Descending order (newest to oldest, Z-A).
    """

    ASC = "ASC"
    DESC = "DESC"


# ---------------------------------------------------------------------------
# Default configuration values
# ---------------------------------------------------------------------------

DEFAULT_PAGE: int = 0
"""Default page number for pagination (0-indexed)."""

DEFAULT_LIMIT: int = 20
"""Default number of items per page."""

DEFAULT_ORDER: SortOrder = SortOrder.DESC
"""Default sort order for data retrieval."""

MAX_LIMIT: int = 1000
"""Maximum items per page to prevent excessive data retrieval."""
