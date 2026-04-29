import pandas as pd

from bakeoff.config import BakeoffConfig


def write_delta_table(
    df: pd.DataFrame,
    table_name: str,
    config: BakeoffConfig,
) -> None:
    """
    Write pandas DataFrame to Delta table (Databricks only).
    """
    from pyspark.sql import SparkSession

    spark = SparkSession.getActiveSession()
    if spark is None:
        raise RuntimeError("Spark session not found. Delta output requires Databricks.")

    spark_df = spark.createDataFrame(df)

    full_table_name = f"{config.catalog}.{config.schema}.{table_name}"

    (
        spark_df.write.format("delta")
        .mode("overwrite")
        .saveAsTable(full_table_name)
    )