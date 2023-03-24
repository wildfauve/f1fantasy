import polars as pl


def sum_races(df, race_columns):
    return df.select(pl.col('team'), _sum_fold(race_columns))


def _sum_fold(columns) -> pl.internals.expr.expr.Expr:
    return pl.fold(acc=pl.lit(0), f=lambda acc, x: acc + x, exprs=pl.col(columns).alias("sum"))
