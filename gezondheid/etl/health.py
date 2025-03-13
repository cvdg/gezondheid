import datetime as dt

import polars as pl
from polars import DataFrame


import gezondheid.config as config


QUERY_ALL = """
  select health_date,
         health_sleep_score,
         health_body_battery_max,
         health_body_battery_min,
         health_active_time,
         health_defecation
    from health
order by health_date
"""


def extract(uri: str) -> DataFrame:
    df = pl.read_database_uri(query=QUERY_ALL, uri=uri)

    return df


def validate(df: pl.DataFrame) -> DataFrame:
    start = df["health_date"].min()
    end = df["health_date"].max()
    days = pl.date_range(
        start=start,
        end=end,
        interval="1d",
        eager=True,
    )

    for day in days:
        row = df.row(by_predicate=(pl.col("health_date") == day), named=True)

        if not row:
            raise ValueError(f"date does not exist: {day}")

        if row["health_sleep_score"] < 0 or row["health_sleep_score"] > 100:
            raise ValueError(f"date health_sleep_score: {day}")

        if row["health_body_battery_max"] < 0 or row["health_body_battery_max"] > 100:
            raise ValueError(f"date health_body_battery_max: {day}")

        if row["health_body_battery_min"] < 0 or row["health_body_battery_min"] > 100:
            raise ValueError(f"date health_body_battery_min: {day}")

        if row["health_active_time"] < 0 or row["health_active_time"] > 360:
            raise ValueError(f"date health_active_time: {day}")

        if row["health_defecation"] < 0 or row["health_defecation"] > 5:
            raise ValueError(f"date health_defecation: {day}")

    return df


def transform(df: DataFrame) -> DataFrame:
    weekly = df.with_columns(
        health_idx=pl.col("health_date").dt.iso_year() * 100
        + pl.col("health_date").dt.week(),
    )
    weekly = weekly.drop("health_date")
    weekly = (
        weekly.group_by("health_idx")
        .agg(pl.all().mean().cast(pl.Int32))
        .sort("health_idx")
    )
    return weekly

def transform2(df: DataFrame) -> DataFrame:
    df = df.with_columns(health_date=(pl.col('health_date') - pl.duration(days=pl.col('health_date').dt.weekday() - 1)),)
    df = df.group_by("health_date").agg(pl.all().mean().cast(pl.Int32)).sort("health_date")
    return df

def load(df: DataFrame) -> None:
    with open("sleep_score.png", mode='wb') as img:
        plot = df.plot.line(x="health_date", y="health_sleep_score")
        plot.save(img, format="png")

    with open("body_battery_max.png", mode='wb') as img:
        plot = df.plot.line(x="health_date", y="health_body_battery_max")
        plot.save(img, format="png")

    with open("body_battery_min.png", mode='wb') as img:
        plot = df.plot.line(x="health_date", y="health_body_battery_min")
        plot.save(img, format="png")

    with open("active_time.png", mode='wb') as img:
        plot = df.plot.line(x="health_date", y="health_active_time")
        plot.save(img, format="png")

    with open("defecation.png", mode='wb') as img:
        plot = df.plot.line(x="health_date", y="health_defecation")
        plot.save(img, format="png")


if __name__ == "__main__":
    df = extract(config.DB_URI)
    df = validate(df)
    df = transform2(df)

    print("=" * 80)
    print(df.describe())

    print("=" * 80)

    # tmp = df.filter(pl.col('health_idx') == 202401)

    print(df)

    load(df)
