"""
DataCanvas SDK — Main client for interacting with the DataCanvas IoT platform.

Example::

    from datacanvas import DataCanvas, SortOrder

    client = DataCanvas(
        access_key_client="your-access-key-id",
        access_key_secret="your-secret-key",
        project_id=123,
        base_url="https://api.<something>.<something>",
    )

    # List all devices
    devices = client.devices.list()

    # Retrieve data with filtering
    data = client.data.list(
        table_name="temperature_sensors",
        devices=[1, 2, 3],
        limit=50,
        order=SortOrder.DESC,
    )
"""

from __future__ import annotations

from datacanvas.core.http_client import HttpClient
from datacanvas.resources.data import DataResource
from datacanvas.resources.devices import DevicesResource

__all__ = ["DataCanvas"]


class DataCanvas:
    """Main client for the DataCanvas IoT platform.

    Provides access to :attr:`devices` and :attr:`data` resources through a
    clean, resource-based interface.

    Parameters:
        access_key_client: Client access key ID for API authentication.
        access_key_secret: Secret access key for API authentication.
        project_id: Project ID to scope API requests.
        base_url: Base URL for the DataCanvas API.

    Raises:
        ValueError: When configuration parameters are invalid.

    Example::

        client = DataCanvas(
            access_key_client="your-key",
            access_key_secret="your-secret",
            project_id=42,
            base_url="https://api.example.com",
        )
        devices = client.devices.list()
    """

    def __init__(
        self,
        *,
        access_key_client: str,
        access_key_secret: str,
        project_id: int,
        base_url: str,
    ) -> None:
        # Validate configuration
        self._validate_config(
            access_key_client=access_key_client,
            access_key_secret=access_key_secret,
            project_id=project_id,
            base_url=base_url,
        )

        # Initialise HTTP client with configuration
        self._http_client = HttpClient(
            base_url=base_url,
            project_id=project_id,
            access_key_client=access_key_client,
            access_key_secret=access_key_secret,
        )

        # Initialise resource classes with dependency injection
        self.devices = DevicesResource(self._http_client)
        """Resource for device management operations."""

        self.data = DataResource(self._http_client)
        """Resource for data retrieval operations."""

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_config(
        *,
        access_key_client: str,
        access_key_secret: str,
        project_id: int,
        base_url: str,
    ) -> None:
        """Validate SDK configuration parameters.

        Raises:
            ValueError: When any configuration parameter is invalid.
        """
        if not access_key_client or not isinstance(access_key_client, str):
            raise ValueError(
                "Invalid configuration: access_key_client is required and must be a non-empty string."
            )

        if not access_key_secret or not isinstance(access_key_secret, str):
            raise ValueError(
                "Invalid configuration: access_key_secret is required and must be a non-empty string."
            )

        if not isinstance(project_id, int) or project_id <= 0:
            raise ValueError(
                "Invalid configuration: project_id is required and must be a positive integer."
            )

        if not base_url or not isinstance(base_url, str):
            raise ValueError(
                "Invalid configuration: base_url is required and must be a non-empty string."
            )

    # ------------------------------------------------------------------
    # Context manager support
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP session and release resources."""
        self._http_client.close()

    def __enter__(self) -> "DataCanvas":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"<DataCanvas(base_url={self._http_client._base_url!r})>"
