"""Tests for configuration validation and client initialisation."""

import pytest
from datacanvas import DataCanvas


class TestClientValidation:
    """Ensure invalid configurations raise ValueError."""

    def test_missing_access_key_client(self) -> None:
        with pytest.raises(ValueError, match="access_key_client"):
            DataCanvas(access_key_client="", access_key_secret="s", project_id=1, base_url="http://localhost/api")

    def test_missing_access_key_secret(self) -> None:
        with pytest.raises(ValueError, match="access_key_secret"):
            DataCanvas(access_key_client="k", access_key_secret="", project_id=1, base_url="http://localhost/api")

    def test_invalid_project_id_zero(self) -> None:
        with pytest.raises(ValueError, match="project_id"):
            DataCanvas(access_key_client="k", access_key_secret="s", project_id=0, base_url="http://localhost/api")

    def test_invalid_project_id_negative(self) -> None:
        with pytest.raises(ValueError, match="project_id"):
            DataCanvas(access_key_client="k", access_key_secret="s", project_id=-5, base_url="http://localhost/api")

    def test_missing_base_url(self) -> None:
        with pytest.raises(ValueError, match="base_url"):
            DataCanvas(access_key_client="k", access_key_secret="s", project_id=1, base_url="")

    def test_valid_config_creates_client(self) -> None:
        client = DataCanvas(access_key_client="k", access_key_secret="s", project_id=1, base_url="http://localhost/api")
        assert client.devices is not None
        assert client.data is not None

    def test_custom_base_url(self) -> None:
        client = DataCanvas(
            access_key_client="k",
            access_key_secret="s",
            project_id=1,
            base_url="https://custom.example.com/api",
        )
        assert "custom.example.com" in repr(client)

    def test_context_manager(self) -> None:
        with DataCanvas(access_key_client="k", access_key_secret="s", project_id=1, base_url="http://localhost/api") as client:
            assert client.devices is not None
