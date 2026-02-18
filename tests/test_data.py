"""Tests for data resource validation."""

import pytest
from datacanvas import DataCanvas
from datacanvas.core.exceptions import ValidationError


@pytest.fixture()
def client() -> DataCanvas:
    return DataCanvas(access_key_client="k", access_key_secret="s", project_id=1, base_url="http://localhost/api")


class TestDataValidation:
    """Ensure invalid data parameters raise ValidationError."""

    def test_empty_table_name(self, client: DataCanvas) -> None:
        with pytest.raises(ValidationError, match="table_name"):
            client.data.list(table_name="")

    def test_whitespace_table_name(self, client: DataCanvas) -> None:
        with pytest.raises(ValidationError, match="table_name"):
            client.data.list(table_name="   ")

    def test_negative_page(self, client: DataCanvas) -> None:
        with pytest.raises(ValidationError, match="page"):
            client.data.list(table_name="t", page=-1)

    def test_zero_limit(self, client: DataCanvas) -> None:
        with pytest.raises(ValidationError, match="limit"):
            client.data.list(table_name="t", limit=0)

    def test_negative_limit(self, client: DataCanvas) -> None:
        with pytest.raises(ValidationError, match="limit"):
            client.data.list(table_name="t", limit=-10)

    def test_limit_exceeds_max(self, client: DataCanvas) -> None:
        with pytest.raises(ValidationError, match="1000"):
            client.data.list(table_name="t", limit=1001)

    def test_invalid_device_id(self, client: DataCanvas) -> None:
        with pytest.raises(ValidationError, match="positive integers"):
            client.data.list(table_name="t", devices=[0])

    def test_negative_device_id(self, client: DataCanvas) -> None:
        with pytest.raises(ValidationError, match="positive integers"):
            client.data.list(table_name="t", devices=[-1])
