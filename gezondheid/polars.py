import polars as pl

from gezondheid.config import DB_URI

QUERY = """
  select cast(round(date_part('year', health_date)) as integer) as health_year,
         cast(round(date_part('week', health_date)) as integer) as health_week,
         cast(round(avg(health_sleep_score)) as integer)        as health_sleep_score,
         cast(round(avg(health_body_battery_max)) as integer)   as health_body_battery_max,
         cast(round(avg(health_body_battery_min)) as integer)   as health_body_battery_min,
         cast(round(sum(health_active_time)) as integer)        as health_active_time,
         cast(round(avg(health_defecation)) as integer)         as health_defecation
    from health 
group by health_year, health_week
order by health_year, health_week
"""


def do_polars() -> None:
    df = pl.read_database_uri(query=QUERY, uri=DB_URI)
    print(df)


if __name__ == "__main__":
    do_polars()
