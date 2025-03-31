"""Main script to run the ETL process for South American countries data."""
import logging
from data_loader import DataLoader
from etl import ETL


logging.basicConfig(
    level=logging.INFO,  # Puede ser DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Crear un logger
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Descargar y guardar los datos
    logger.info("Process started.")
    loader = DataLoader(["ARG", "CHL", "BOL", "PRY", "BRA", "URY"])
    df = loader.load_data()
    loader.save_data(df)

    # Ejecutar el ETL
    etl = ETL()
    spark_df = etl.load_data()
    transformed_df = etl.transform_data(spark_df)
    etl.save_data(transformed_df)

    logger.info("ETL finished correctly.")
