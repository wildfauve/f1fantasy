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
@click.option("--accum/--ind", "-a/-i", required=False, default=False, help="Individual Race Scores or Accumulated Race scores")
@click.command()
def post_points(team, season, gp, points, accum):
    """
    Creates a new Fantasy Team with members
    """
    command.post_score_controller(gp_symbol=gp, season_year=int(season), team=team, score=points, accum=accum)
    pass


@click.option('--file', '-f', required=True)
@click.option("--season", "-s", type=click.Choice(helpers.seasons()), required=True, help="Pick a Season")
@click.option("--accum/--ind", "-a/-i", required=False, default=False, help="Individual Race Scores or Accumulated Race scores")
@click.command()
def post_points_file(file, season, accum):
    """
    Creates a new Fantasy Team with members
    """
    command.post_points_file(file=file, season=int(season), accum=accum)
    pass


@click.option('--file', '-f', required=True)
@click.option("--season", "-s", type=click.Choice(helpers.seasons()), required=True, help="Pick a Season")
@click.option("--position/--accum", "-p/-a", required=False, default=False, help="Plot Position, or plot total scores")
@click.command()
def ranking_plot(file, season, position):
    """
    Generate a Ranking Graph
    """
    command.scores_plot(file=file, season=int(season), position=position)
    pass


@click.option("--season", "-s", type=click.Choice(helpers.seasons()), required=True, help="Pick a Seasion")
@click.option("--accum/--ind", "-a/-i", required=False, default=False, help="Individual Race Scores or Accumulated Race scores")
@click.option("--sort/--unsorted", "-t/-u", required=False, default=False, help="Sort the results in descending order")
@click.command()
def show_table(season, accum, sort):
    """
    Show the Fantasy Points Table
    """
    presenter.event_team_scores_table(command.team_scores_query(season=int(season), accum=accum, sort=sort))
    pass


cli.add_command(post_points)
cli.add_command(post_points_file)
cli.add_command(show_table)
cli.add_command(ranking_plot)
