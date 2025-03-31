"""ETL process for COVID-19 data using PySpark."""
from pyspark.sql import SparkSession

class ETL:
    """Class to perform ETL process using PySpark."""

    def __init__(self, input_path: str = ".data/covid_data.csv", output_path: str = ".data/covid_data.parquet"):
        self.spark = SparkSession.builder.appName("CovidETL").getOrCreate()
        self.input_path = input_path
        self.output_path = output_path

    def load_data(self):
        """Load CSV data into a Spark DataFrame."""
        return self.spark.read.csv(self.input_path, header=True, inferSchema=True)

    def transform_data(self, df):
        """Minimal transformation: select relevant columns."""
        return df.select("iso_code", "date", "total_cases", "total_deaths").dropna()

    def save_data(self, df):
        """Save transformed data as Parquet."""
        df.write.mode("overwrite").parquet(self.output_path)
