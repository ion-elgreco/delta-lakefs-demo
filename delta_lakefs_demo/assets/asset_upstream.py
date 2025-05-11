import dagster as dg
import polars as pl


@dg.asset(io_manager_key="bronze_delta_io_manager")
def upstream_asset() -> pl.DataFrame:
    return pl.DataFrame({"foo": list(range(10))})
