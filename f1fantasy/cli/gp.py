import click

from f1fantasy import command
from f1fantasy import initialiser



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
    Creates a new F1 Season
    """
    command.create_gp(name=name, label=label, symbol=symbol)
    pass


cli.add_command(create_season)
cli.add_command(create_gp)
