"""Module to download and save COVID-19 data for selected countries."""
import logging
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

class DataLoader:
    """Class to download and save COVID-19 data for selected countries."""

    def __init__(self, output_path: str = "./data/covid_data.csv"):
        self.url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
        self.output_path = output_path
        self.selected_countries = ["Argentina", "Chile", "Bolivia", "Paraguay", "Brazil", "Uruguay"]
        self.start_date = "2020-01-01"
        self.end_date = "2022-12-31"

    def load_data(self) -> pd.DataFrame:
        """Download COVID-19 data and filter by selected countries and years."""
        logger.info("Downloading COVID-19 data...")
        try:
            df = pd.read_csv(self.url, parse_dates=["date"])
            logger.info("Data downloaded successfully.")

            # Filtrar por países y rango de fechas
            df = df[df["location"].isin(self.selected_countries)]
            df = df[(df["date"] >= self.start_date) & (df["date"] <= self.end_date)]

            logger.info("Data filtered for %d countries and years 2020-2022", len(self.selected_countries))
            return df

        except Exception as error:
            logger.error("Error downloading data: %s", error)
            raise

    def save_data(self, df: pd.DataFrame) -> None:
        """Save the filtered dataset locally."""
        df.to_csv(self.output_path, index=False)
        logger.info("Data saved to %s", self.output_path)