from typing import Dict
import polars as pl


def build_df(row_columns: Dict) -> pl.DataFrame:
    return pl.DataFrame(row_columns)
