"""
Resource class for device management operations.

Provides methods to interact with IoT devices in the DataCanvas platform.
Follows the Single Responsibility Principle by focusing solely on
device-related operations and delegating HTTP communication to
:class:`~datacanvas.core.http_client.HttpClient`.
"""

from __future__ import annotations

from typing import Any, Dict, List

from datacanvas.core.constants import Endpoints
from datacanvas.core.http_client import HttpClient
from datacanvas.types import Device, DeviceResponse

__all__ = ["DevicesResource"]


class DevicesResource:
    """Resource for device management operations.

    Parameters:
        client: The :class:`HttpClient` used for API communication.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def list(self) -> DeviceResponse:
        """Retrieve all devices associated with the configured project.

        Returns:
            A :class:`~datacanvas.types.DeviceResponse` containing all
            devices.

        Raises:
            AuthenticationError: When credentials are invalid.
            AuthorizationError: When lacking permissions.
            NetworkError: When network connectivity fails.

        Example::

            devices = client.devices.list()
            for d in devices.devices:
                print(f"Device: {d.device_name} (ID: {d.device_id})")
        """
        raw: Dict[str, Any] = self._client.post(Endpoints.DEVICES, {})
        return self._parse_response(raw)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_response(raw: Dict[str, Any]) -> DeviceResponse:
        """Convert the raw JSON dict into a typed :class:`DeviceResponse`."""
        devices: List[Device] = [
            Device(
                device_id=d["device_id"],
                device_name=d["device_name"],
            )
            for d in raw.get("devices", [])
        ]
        return DeviceResponse(
            success=raw.get("success", False),
            devices=devices,
        )
