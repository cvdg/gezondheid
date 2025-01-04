"""
Command line interface
"""

from gezondheid.model import engine, Base, Health

import click
from sqlalchemy.orm import Session


@click.group()
def cli() -> None:
    pass


@cli.group()
def db() -> None:
    """Database/Table commands."""
    pass


@db.command("create")
def db_create() -> None:
    """Create all tables."""
    click.echo("Create all tables.")
    Base.metadata.create_all(engine)


@db.command("drop")
def db_drop() -> None:
    """Drop all tables."""
    click.echo("Drop database")
    Base.metadata.drop_all(engine)


@cli.group()
def health() -> None:
    """Health commands."""
    pass


@health.command("create")
@click.option("--date", prompt="Date", type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option("--sleep-score", prompt="Sleep Score", type=int)
@click.option("--body-battery-max", prompt="Body battery Max", type=int)
@click.option("--body-battery-min", prompt="Body battery Min", type=int)
@click.option("--active-time", prompt="Active time", type=int)
@click.option("--defecation", prompt="Defecation", type=int)
def health_create(
    date: click.DateTime,
    sleep_score: int,
    body_battery_max: int,
    body_battery_min: int,
    active_time: int,
    defecation: int,
) -> None:
    """Create a new health record in the table."""
    date = date.date()
    click.echo(f"            Date: {date}")
    click.echo(f"     Sleep score: {sleep_score:3}")
    click.echo(f"Body battery Max: {body_battery_max:3}")
    click.echo(f"Body battery Min: {body_battery_min:3}")
    click.echo(f"     Active time: {active_time:3}")
    click.echo(f"      Defecation: {defecation:3}")

    with Session(engine) as session:
        health = Health(
            health_date=date,
            health_sleep_score=sleep_score,
            health_body_battery_max=body_battery_max,
            health_body_battery_min=body_battery_min,
            health_active_time=active_time,
            health_defecation=defecation,
        )
        session.add(health)
        session.commit()


@health.command("read")
@click.option("--date", prompt="Date", type=click.DateTime(formats=["%Y-%m-%d"]))
def health_read(date: click.DateTime) -> None:
    """Read a health reacorf from the table."""
    date = date.date()
    with Session(engine) as session:
        health = session.query(Health).filter(Health.health_date == date).one_or_none()

    if health:
        click.echo(f"            Date: {health.health_date}")
        click.echo(f"     Sleep score: {health.health_sleep_score:3}")
        click.echo(f"Body battery Max: {health.health_body_battery_max:3}")
        click.echo(f"Body battery Min: {health.health_body_battery_min:3}")
        click.echo(f"     Active time: {health.health_active_time:3}")
        click.echo(f"      Defecation: {health.health_defecation:3}")
    else:
        click.echo(f"Not found date: {date}")


@health.command("update")
@click.option("--date", prompt="Date", type=click.DateTime(formats=["%Y-%m-%d"]))
def health_update(date: click.DateTime) -> None:
    """Update a health record in the table."""
    date = date.date()
    with Session(engine) as session:
        health = session.query(Health).filter(Health.health_date == date).one_or_none()

        if health:
            click.echo(f"            Date: {health.health_date}")
            click.echo(f"     Sleep score: {health.health_sleep_score:3}")
            click.echo(f"Body battery Max: {health.health_body_battery_max:3}")
            click.echo(f"Body battery Min: {health.health_body_battery_min:3}")
            click.echo(f"     Active time: {health.health_active_time:3}")
            click.echo(f"      Defecation: {health.health_defecation:3}")

            sleep_score = click.prompt(
                "Sleep score", type=int, default=health.health_sleep_score
            )
            body_battery_max = click.prompt(
                "Body battery Max", type=int, default=health.health_body_battery_max
            )
            body_battery_min = click.prompt(
                "Body battery Min", type=int, default=health.health_body_battery_min
            )
            active_time = click.prompt(
                "Active time", type=int, default=health.health_active_time
            )
            defecation = click.prompt(
                "Defecation", type=int, default=health.health_defecation
            )

            health.health_sleep_score = sleep_score
            health.health_body_battery_max = body_battery_max
            health.health_body_battery_min = body_battery_min
            health.health_active_time = active_time
            health.health_defecation = defecation

            session.add(health)
            session.commit()

            click.echo(f"            Date: {health.health_date}")
            click.echo(f"     Sleep score: {health.health_sleep_score:3}")
            click.echo(f"Body battery Max: {health.health_body_battery_max:3}")
            click.echo(f"Body battery Min: {health.health_body_battery_min:3}")
            click.echo(f"     Active time: {health.health_active_time:3}")
            click.echo(f"      Defecation: {health.health_defecation:3}")
        else:
            click.echo(f"Not found date: {date}")


@health.command("delete")
@click.option("--date", prompt="Date", type=click.DateTime(formats=["%Y-%m-%d"]))
def health_delete(date: click.DateTime) -> None:
    """Delete a health record from the table."""
    date = date.date()
    with Session(engine) as session:
        health = session.query(Health).filter(Health.health_date == date).one_or_none()

        if health:
            click.echo(f"            Date: {health.health_date}")
            click.echo(f"     Sleep score: {health.health_sleep_score:3}")
            click.echo(f"Body battery Max: {health.health_body_battery_max:3}")
            click.echo(f"Body battery Min: {health.health_body_battery_min:3}")
            click.echo(f"     Active time: {health.health_active_time:3}")
            click.echo(f"      Defecation: {health.health_defecation:3}")
            session.delete(health)
            session.commit()
        else:
            click.echo(f"Not found date: {date}")


@health.command("list")
def health_list() -> None:
    """List all health records from the table."""
    with Session(engine) as session:
        result = session.query(Health).order_by(Health.health_date).all()
        for health in result:
            click.echo(
                f"{health.health_date} {health.health_sleep_score:4} {health.health_body_battery_max:4} {health.health_body_battery_min:4} {health.health_active_time:4} {health.health_defecation:4}"
            )


if __name__ == "__main__":
    cli()
