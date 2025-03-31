"""Unit tests for the DataLoader class."""
import os
import pandas as pd
import pytest
from src.data_loader import DataLoader

@pytest.fixture
def loader() -> DataLoader:
    """Fixture to create a DataLoader instance."""
    return DataLoader(["ARG", "CHL"], ".data/test_covid_data.csv")

def test_load_data(loader) -> bool:
    """Test the load_data method."""
    df = loader.load_data()
    assert not df.empty, "El DataFrame no debería estar vacío"
    assert "iso_code" in df.columns, "Falta la columna 'iso_code'"

def test_save_data(loader) -> bool:
    """Test the save_data method."""
    df = pd.DataFrame({"iso_code": ["ARG", "CHL"], "total_cases": [1000, 2000]})
    loader.save_data(df)
    assert os.path.exists(loader.output_path), "El archivo no fue guardado correctamente"
