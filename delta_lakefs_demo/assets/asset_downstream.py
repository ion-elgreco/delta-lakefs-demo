import dagster as dg
import polars as pl


@dg.asset(io_manager_key="silver_delta_io_manager")
def downstream_asset(upstream_asset: pl.DataFrame) -> pl.DataFrame:
    return upstream_asset.with_columns(pl.lit("hello world").alias("bar"))
