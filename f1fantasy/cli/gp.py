import click

from f1fantasy import initialiser, command
from . import helpers


@click.group()
def cli():
    pass


# @click.option("--season", "-s",
#               type=click.Choice(seasons()),
#               help="Pick a Seasion")
# @click.command()
# def add_gp_event(season):
#     """
#     Generates the graph at the standard repo location.
#     """
#     breakpoint()
#     graph_command.generate_graph(int(season))
#     pass


# @click.command()
# def teams():
#     """
#     Displays the teams and their members
#     """
#     graph_command.display_teams()
#     pass


@click.option("--season", "-s",
              type=int,
              help="Create a Season by providing a year")
@click.command()
def create_season(season):
    """
    Creates a new F1 Season
    """
    command.create_season(season)
    pass


@click.option("--name", "-n", help="GP Name")
@click.option("--label", "-l", help="GP Label")
@click.option("--symbol", "-b", help="GP Symbol")
@click.command()
def create_gp(name, label, symbol):
    """
    Creates a Grand Prix
    """
    command.create_gp(name=name, label=label, symbol=symbol)
    pass


@click.option("--season", "-s", type=click.Choice(helpers.seasons()), help="Pick a Seasion")
@click.option("--gp", "-g", type=click.Choice(helpers.gp_symbols()), help="GP Symbol")
@click.option("--date", "-d", help="Date of GP")
@click.option("--for-round", "-r", type=int, help="Round Number")
@click.command()
def create_event(gp, season, date, for_round):
    """
    Creates an event for a GP in a Season
    """
    command.create_season_event(gp_symbol=gp, season_year=int(season), gp_date=date, for_round=for_round)


cli.add_command(create_season)
cli.add_command(create_gp)
cli.add_command(create_event)
