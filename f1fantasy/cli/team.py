import click

from f1fantasy import command, domain
from f1fantasy import initialiser



@click.group()
def cli():
    pass

@click.option('--team', '-t')
@click.option('--members', '-m', multiple=True)
@click.option('--principle', '-p')
@click.command()
def create(team, members, principle):
    """
    Creates a new Fantasy Team with members
    """
    command.create_team(team, members, principle)
    pass

@click.command()
def show():
    """
    Show Teams, members and manager
    """
    domain.show_teams()

cli.add_command(create)
cli.add_command(show)
