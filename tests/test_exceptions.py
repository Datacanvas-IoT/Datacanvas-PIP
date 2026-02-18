"""Tests for the exception hierarchy."""

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


class TestExceptionHierarchy:
    """All specific errors must inherit from DataCanvasError."""

    def test_authentication_error_inherits(self) -> None:
        assert issubclass(AuthenticationError, DataCanvasError)

    def test_authorization_error_inherits(self) -> None:
        assert issubclass(AuthorizationError, DataCanvasError)

    def test_validation_error_inherits(self) -> None:
        assert issubclass(ValidationError, DataCanvasError)

    def test_not_found_error_inherits(self) -> None:
        assert issubclass(NotFoundError, DataCanvasError)

    def test_rate_limit_error_inherits(self) -> None:
        assert issubclass(RateLimitError, DataCanvasError)

    def test_server_error_inherits(self) -> None:
        assert issubclass(ServerError, DataCanvasError)

    def test_network_error_inherits(self) -> None:
        assert issubclass(NetworkError, DataCanvasError)

    def test_catch_all_with_base(self) -> None:
        """A blanket ``except DataCanvasError`` should catch any sub-error."""
        try:
            raise AuthenticationError("bad creds")
        except DataCanvasError as e:
            assert "bad creds" in str(e)

    def test_not_found_resource_name(self) -> None:
        err = NotFoundError("Datatable")
        assert "Datatable not found" in str(err)
