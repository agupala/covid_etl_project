"""Tests for the ETL process in the COVID-19 data pipeline."""
import pytest
from src.etl import ETL

@pytest.fixture
def etl() -> ETL:
    """Fixture to create an ETL instance."""
    return ETL(".data/test_covid_data.csv", ".data/test_covid_data.parquet")

def test_transform_data(etl_instance) -> bool:
    """Test the transform_data method."""
    df = etl_instance.load_data()
    transformed_df = etl_instance.transform_data(df)
    assert "total_cases" in transformed_df.columns, "Falta la columna 'total_cases'"
