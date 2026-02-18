"""
Resource class for data retrieval operations.

Provides methods to query and retrieve sensor data from datatables.
Follows the Single Responsibility Principle by focusing solely on data
retrieval operations.  It validates input and delegates HTTP communication
to :class:`~datacanvas.core.http_client.HttpClient`.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from datacanvas.core.constants import (
    DEFAULT_LIMIT,
    DEFAULT_ORDER,
    DEFAULT_PAGE,
    MAX_LIMIT,
    Endpoints,
    SortOrder,
)
from datacanvas.core.exceptions import ValidationError
from datacanvas.core.http_client import HttpClient
from datacanvas.types import DataPoint, DataResponse, GetDataParams

__all__ = ["DataResource"]


class DataResource:
    """Resource for data retrieval operations.

    Parameters:
        client: The :class:`HttpClient` used for API communication.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def list(
        self,
        *,
        table_name: str,
        devices: Optional[List[int]] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        order: Optional[SortOrder] = None,
    ) -> DataResponse:
        """Retrieve data from a datatable with optional filtering and pagination.

        Args:
            table_name: Name of the datatable to query (required).
            devices: Optional list of device IDs to filter results.
            page: Page number for pagination (0-indexed, default: 0).
            limit: Number of items per page (default: 20, max: 1000).
            order: Sort order for results (default: ``SortOrder.DESC``).

        Returns:
            A :class:`~datacanvas.types.DataResponse` containing query results.

        Raises:
            ValidationError: When required parameters are missing or invalid.
            AuthenticationError: When credentials are invalid.
            AuthorizationError: When lacking permissions.
            NotFoundError: When datatable is not found.
            NetworkError: When network connectivity fails.

        Example::

            from datacanvas import SortOrder

            data = client.data.list(
                table_name="temperature_sensors",
                devices=[1, 2, 3],
                page=0,
                limit=50,
                order=SortOrder.DESC,
            )
            print(f"Total records: {data.count}")
        """
        params = GetDataParams(
            table_name=table_name,
            devices=devices,
            page=page,
            limit=limit,
            order=order,
        )

        # Validate parameters
        self._validate_params(params)

        # Apply defaults for optional parameters
        effective_limit = params.limit if params.limit is not None else DEFAULT_LIMIT

        if effective_limit > MAX_LIMIT:
            raise ValidationError(
                f"Limit cannot exceed {MAX_LIMIT}. Requested: {effective_limit}"
            )

        request_body: Dict[str, Any] = {
            "datatable_name": params.table_name,
            "devices": params.devices or [],
            "page": params.page if params.page is not None else DEFAULT_PAGE,
            "limit": effective_limit,
            "order": (params.order or DEFAULT_ORDER).value,
        }

        raw: Dict[str, Any] = self._client.post(Endpoints.DATA, request_body)
        return self._parse_response(raw)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_params(params: GetDataParams) -> None:
        """Validate data retrieval parameters.

        Raises:
            ValidationError: When validation fails.
        """
        if not params.table_name:
            raise ValidationError("table_name is required and cannot be empty.")

        if not isinstance(params.table_name, str):
            raise ValidationError("table_name must be a string.")

        if params.table_name.strip() == "":
            raise ValidationError("table_name cannot be empty or whitespace.")

        if params.page is not None:
            if not isinstance(params.page, int) or params.page < 0:
                raise ValidationError("page must be a non-negative integer.")

        if params.limit is not None:
            if not isinstance(params.limit, int) or params.limit <= 0:
                raise ValidationError("limit must be a positive integer.")

        if params.devices is not None:
            if not isinstance(params.devices, list):
                raise ValidationError("devices must be a list.")

            if any(not isinstance(d, int) or d <= 0 for d in params.devices):
                raise ValidationError("All devices must be positive integers.")

    # ------------------------------------------------------------------
    # Response parsing
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_response(raw: Dict[str, Any]) -> DataResponse:
        """Convert the raw JSON dict into a typed :class:`DataResponse`."""
        parsed_data: Dict[str, List[DataPoint]] = {}

        for device_id, points in raw.get("data", {}).items():
            parsed_data[str(device_id)] = [
                DataPoint(
                    id=p.get("id", 0),
                    device=p.get("device", 0),
                    extra={
                        k: v
                        for k, v in p.items()
                        if k not in ("id", "device")
                    },
                )
                for p in points
            ]

        return DataResponse(
            count=raw.get("count", 0),
            data=parsed_data,
        )
