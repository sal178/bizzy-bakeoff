import pandas as pd

from bakeoff.config import BakeoffConfig


def prepare_for_spark(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # for mixed type columns
    value_columns = [
        "bizzy_value",
        "source_value",
        "truth_value",
    ]

    for col in value_columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: None if pd.isna(x) else str(x))

    return df


def write_delta_table(
    df: pd.DataFrame,
    table_name: str,
    config: BakeoffConfig,
) -> None:
    from pyspark.sql import SparkSession

    spark = SparkSession.getActiveSession()
    if spark is None:
        raise RuntimeError("Spark session not found. Delta output requires Databricks.")

    df = prepare_for_spark(df)

    full_table_name = f"{config.catalog}.{config.schema}.{table_name}"

    spark_df = spark.createDataFrame(df)

    (
        spark_df.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(full_table_name)
    )