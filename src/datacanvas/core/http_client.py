"""
HTTP client for making requests to the DataCanvas API.

Handles authentication, error mapping, and request/response processing.

This module follows the Single Responsibility Principle by focusing solely
on HTTP communication.  It automatically injects authentication credentials
and maps HTTP status codes to appropriate error types.

The base URL is provided via :class:`~datacanvas.types.SDKConfig` and is
required for all SDK instances.
"""

from __future__ import annotations

from typing import Any, Dict

import requests

from datacanvas.core.exceptions import (
    AuthenticationError,
    AuthorizationError,
    DataCanvasError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)

__all__ = ["HttpClient"]


class HttpClient:
    """Low-level HTTP client used internally by resource classes.

    Parameters:
        base_url: API base URL (required).
        project_id: Project ID to scope API requests.
        access_key_client: Client access key ID.
        access_key_secret: Secret access key.
    """

    def __init__(
        self,
        *,
        base_url: str,
        project_id: int,
        access_key_client: str,
        access_key_secret: str,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "User-Agent": "datacanvas-sdk-python/1.0.0",
        }
        self._credentials: Dict[str, Any] = {
            "project_id": project_id,
            "access_key_client": access_key_client,
            "access_key_secret": access_key_secret,
        }
        # Shared session for connection pooling and automatic resource cleanup
        self._session = requests.Session()
        self._session.headers.update(self._headers)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def post(self, endpoint: str, body: Dict[str, Any] | None = None) -> Any:
        """Execute a POST request to *endpoint*.

        Authentication credentials are automatically merged into the
        request body.  HTTP error responses are mapped to the appropriate
        :mod:`~datacanvas.core.exceptions` error type.

        Args:
            endpoint: API endpoint path (e.g. ``"/access-keys/external/devices"``).
            body: Optional request body data.  Credentials are merged automatically.

        Returns:
            Parsed JSON response.

        Raises:
            AuthenticationError: When credentials are invalid (HTTP 401).
            AuthorizationError: When lacking permissions (HTTP 403).
            ValidationError: When request validation fails (HTTP 400/422).
            NotFoundError: When the resource is not found (HTTP 404).
            RateLimitError: When the rate limit is exceeded (HTTP 429).
            ServerError: When the server encounters an error (HTTP 500+).
            NetworkError: When a network-level error occurs.
        """
        url = f"{self._base_url}{endpoint}"

        # Merge credentials with request body (credentials take precedence)
        request_body: Dict[str, Any] = {**(body or {}), **self._credentials}

        try:
            response = self._session.post(url, json=request_body, timeout=30)
        except requests.ConnectionError as exc:
            raise NetworkError(f"Network request failed: {exc}") from exc
        except requests.Timeout as exc:
            raise NetworkError(f"Request timed out: {exc}") from exc
        except requests.RequestException as exc:
            raise NetworkError(f"Network request failed: {exc}") from exc

        if not response.ok:
            self._handle_error_response(response)

        return response.json()

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    @staticmethod
    def _handle_error_response(response: requests.Response) -> None:
        """Map an HTTP error response to the appropriate exception and raise it."""
        status = response.status_code

        try:
            error_data = response.json()
            error_message: str = (
                error_data.get("message")
                or error_data.get("error")
                or "An error occurred"
            )
        except (ValueError, KeyError):
            error_message = response.reason or "An error occurred"

        status_map: Dict[int, DataCanvasError] = {
            401: AuthenticationError(error_message),
            403: AuthorizationError(error_message),
            400: ValidationError(error_message),
            422: ValidationError(error_message),
            404: NotFoundError(error_message),
            429: RateLimitError(error_message),
            500: ServerError(error_message),
            502: ServerError(error_message),
            503: ServerError(error_message),
            504: ServerError(error_message),
        }

        exc = status_map.get(status)
        if exc is not None:
            raise exc

        # Fallback for unexpected status codes
        if status >= 500:
            raise ServerError(error_message)
        if status >= 400:
            raise ValidationError(error_message)
        raise DataCanvasError(error_message)

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self._session.close()

    def __enter__(self) -> "HttpClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
