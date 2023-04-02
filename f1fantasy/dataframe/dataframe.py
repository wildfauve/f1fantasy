from typing import Dict
import polars as pl

from .expr import rankings


def build_df(row_columns: Dict) -> pl.DataFrame:
    return pl.DataFrame(row_columns)

def race_rank(df) -> pl.DataFrame:
    cols = df.columns[1:]
    return rankings(df, cols).drop(cols)

