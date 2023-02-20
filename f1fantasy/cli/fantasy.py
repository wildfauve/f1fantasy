import click

from f1fantasy import command
from f1fantasy import initialiser

from . import helpers



@click.group()
def cli():
    pass

@click.option('--team', '-t', type=click.Choice(helpers.team_names()))
@click.option("--season", "-s", type=click.Choice(helpers.seasons()), help="Pick a Seasion")
@click.option("--gp", "-g", type=click.Choice(helpers.gp_symbols()), help="GP Symbol")
@click.option('--points', '-p', type=int)
@click.command()
def post_points(team, season, gp, points):
    """
    Creates a new Fantasy Team with members
    """
    command.post_event_fantasy_score(gp_symbol=gp, season_year=int(season), team=team, score=points)
    pass


cli.add_command(post_points)
