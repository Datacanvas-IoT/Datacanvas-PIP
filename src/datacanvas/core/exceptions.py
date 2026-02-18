"""
Custom exception hierarchy for the DataCanvas SDK.

Every SDK-specific error inherits from :class:`DataCanvasError` so callers
can catch all SDK errors with a single ``except DataCanvasError`` clause
while still being able to handle individual error types.
"""

__all__ = [
    "DataCanvasError",
    "AuthenticationError",
    "AuthorizationError",
    "ValidationError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "NetworkError",
]


class DataCanvasError(Exception):
    """Base error class for all DataCanvas SDK errors."""

    def __init__(self, message: str = "An error occurred in the DataCanvas SDK.") -> None:
        super().__init__(message)
        self.message = message


class AuthenticationError(DataCanvasError):
    """Raised when authentication credentials are invalid or missing.

    Corresponds to HTTP 401 Unauthorized.
    """

    def __init__(self, message: str = "Authentication failed. Invalid access key or secret.") -> None:
        super().__init__(message)


class AuthorizationError(DataCanvasError):
    """Raised when the authenticated user lacks permission for the requested resource.

    Corresponds to HTTP 403 Forbidden.
    """

    def __init__(self, message: str = "Authorization failed. Insufficient permissions.") -> None:
        super().__init__(message)


class ValidationError(DataCanvasError):
    """Raised when request parameters fail validation.

    Corresponds to HTTP 400 Bad Request or 422 Unprocessable Entity.
    """

    def __init__(self, message: str = "Validation failed. Invalid request parameters.") -> None:
        super().__init__(message)


class NotFoundError(DataCanvasError):
    """Raised when the requested resource cannot be found.

    Corresponds to HTTP 404 Not Found.
    """

    def __init__(self, resource: str = "Resource") -> None:
        super().__init__(f"{resource} not found.")


class RateLimitError(DataCanvasError):
    """Raised when the rate-limiting threshold is exceeded.

    Corresponds to HTTP 429 Too Many Requests.
    """

    def __init__(self, message: str = "Rate limit exceeded. Please wait before making more requests.") -> None:
        super().__init__(message)


class ServerError(DataCanvasError):
    """Raised when the server encounters an internal error.

    Corresponds to HTTP 500+ Server Errors.
    """

    def __init__(self, message: str = "Server error occurred. Please try again later.") -> None:
        super().__init__(message)


class NetworkError(DataCanvasError):
    """Raised when a network-level error occurs (connection timeout, DNS failure, etc.).

    Used for non-HTTP errors such as network connectivity issues.
    """

    def __init__(self, message: str = "Network error. Please check your connection and try again.") -> None:
        super().__init__(message)
