"""Tests for HTTP client error mapping."""

import pytest
import responses

from datacanvas.core.http_client import HttpClient
from datacanvas.core.exceptions import (
    AuthenticationError,
    AuthorizationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)


@pytest.fixture()
def http_client() -> HttpClient:
    return HttpClient(
        base_url="https://test.example.com/api",
        project_id=1,
        access_key_client="key",
        access_key_secret="secret",
    )


class TestHttpClientErrorMapping:
    """Map HTTP status codes to the correct exception types."""

    @responses.activate
    def test_401_raises_authentication_error(self, http_client: HttpClient) -> None:
        responses.post(
            "https://test.example.com/api/test",
            json={"message": "Unauthorized"},
            status=401,
        )
        with pytest.raises(AuthenticationError):
            http_client.post("/test")

    @responses.activate
    def test_403_raises_authorization_error(self, http_client: HttpClient) -> None:
        responses.post(
            "https://test.example.com/api/test",
            json={"message": "Forbidden"},
            status=403,
        )
        with pytest.raises(AuthorizationError):
            http_client.post("/test")

    @responses.activate
    def test_400_raises_validation_error(self, http_client: HttpClient) -> None:
        responses.post(
            "https://test.example.com/api/test",
            json={"message": "Bad request"},
            status=400,
        )
        with pytest.raises(ValidationError):
            http_client.post("/test")

    @responses.activate
    def test_404_raises_not_found_error(self, http_client: HttpClient) -> None:
        responses.post(
            "https://test.example.com/api/test",
            json={"message": "Not found"},
            status=404,
        )
        with pytest.raises(NotFoundError):
            http_client.post("/test")

    @responses.activate
    def test_429_raises_rate_limit_error(self, http_client: HttpClient) -> None:
        responses.post(
            "https://test.example.com/api/test",
            json={"message": "Rate limited"},
            status=429,
        )
        with pytest.raises(RateLimitError):
            http_client.post("/test")

    @responses.activate
    def test_500_raises_server_error(self, http_client: HttpClient) -> None:
        responses.post(
            "https://test.example.com/api/test",
            json={"message": "Internal error"},
            status=500,
        )
        with pytest.raises(ServerError):
            http_client.post("/test")

    @responses.activate
    def test_200_returns_json(self, http_client: HttpClient) -> None:
        responses.post(
            "https://test.example.com/api/test",
            json={"success": True},
            status=200,
        )
        result = http_client.post("/test")
        assert result == {"success": True}
