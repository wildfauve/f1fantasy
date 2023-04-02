from typing import Dict
import polars as pl

from .expr import rankings


def build_df(row_columns: Dict, sort: bool = False) -> pl.DataFrame:
    df = pl.DataFrame(row_columns)
    if not sort:
        return df
    return df.sort(df.columns[-1], reverse=True)

def race_rank(df) -> pl.DataFrame:
    cols = df.columns[1:]
    return rankings(df, cols).drop(cols)

