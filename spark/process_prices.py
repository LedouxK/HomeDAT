"""Traitement Spark des prix de Lyon."""

from pyspark.sql import SparkSession


def process_prices(input_path: str, output_path: str) -> None:
    """Calcule la moyenne des prix et exporte un résumé."""
    spark = SparkSession.builder.appName("ProcessPrices").getOrCreate()
    df = spark.read.csv(input_path, header=True, inferSchema=True)
    summary = df.groupBy().avg("prix_m2").withColumnRenamed(
        "avg(prix_m2)", "prix_m2_moyen"
    )
    summary.coalesce(1).write.csv(output_path, header=True, mode="overwrite")
    spark.stop()


if __name__ == "__main__":
    process_prices("data/lyon_prices.csv", "data/summary")
