from typing import List
from rich.table import Table

from f1fantasy import model
from f1fantasy.util import echo
from f1fantasy.initialiser import rich

def teams_echo_presenter(teams: List[model.FantasyTeam]):
    for team in teams:
        echo.echo(team.name)
        echo.echo(f"|__ Managed by: {team.manager.name}")
        echo.echo("|__ Members:")
        for mem in team.members:
            echo.echo(f"    |__ {mem.name}")


def teams_rich_presenter(teams: List[model.FantasyTeam]):
    for team in teams:
        rich.console.print(team.name, style="magenta bold")
        rich.console.print(f"|__ Managed by: [blue]{team.manager.name}")
        rich.console.print("|__ Members:", style="green bold")
        for mem in team.members:
            rich.console.print(f"    |__ {mem.name}", style="green")


def teams_table(teams: List[model.FantasyTeam]):
    table = Table(title="Fantasy Teams")

    table.add_column("Team", justify="right", style="cyan", no_wrap=True)
    table.add_column("Principal", justify="center", style="green")
    table.add_column("Members", style="magenta")


    for team in sorted(teams, key=lambda t: t.manager):
        table.add_row(team.name,
                      team.manager.name,
                      ", ".join([mem.name for mem in team.members]))

    rich.console.print(table)
