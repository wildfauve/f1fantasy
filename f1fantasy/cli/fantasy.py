import click

from f1fantasy import command, domain, presenter, dataframe, repo
from f1fantasy import initialiser

from . import helpers


@click.group()
def cli():
    pass


@click.option('--team', '-t', type=click.Choice(helpers.team_names()), required=True)
@click.option("--season", "-s", type=click.Choice(helpers.seasons()), required=True, help="Pick a Season")
@click.option("--gp", "-g", type=click.Choice(helpers.gp_symbols()), required=True, help="GP Symbol")
@click.option('--points', '-p', type=int, required=True)
@click.command()
def post_points(team, season, gp, points):
    """
    Creates a new Fantasy Team with members
    """
    command.post_event_fantasy_score(gp_symbol=gp, season_year=int(season), team=team, score=points)
    pass


@click.option("--season", "-s", type=click.Choice(helpers.seasons()), required=True, help="Pick a Seasion")
@click.command()
def show_table(season):
    """
    Show the Fantasy Points Table
    """
    presenter.event_team_scores_table(dataframe.team_scores(g=repo.graph(), season=int(season)))
    pass


cli.add_command(post_points)
cli.add_command(show_table)
