import pathlib
import typing

import typer

from nonogram import services

app = typer.Typer()


@app.command()
def solve(
    file: typing.Annotated[pathlib.Path, typer.Argument()],
    line_by_line: typing.Annotated[bool, typer.Option()] = False,  # noqa: FBT002
) -> None:
    length, _, *info = file.read_text().splitlines()

    length = int(length)
    col_info = [[int(n) for n in i.split()] for i in info[:length]]
    row_info = [[int(n) for n in i.split()] for i in info[length + 1 :]]

    solver = services.NonogramSolver(col_info, row_info)
    if not line_by_line:
        typer.echo(solver.answer_str)
        return

    typer.echo(" ".join(("1", "2", "3", "4", "5") * (length // 5)))
    typer.echo("-" * (length * 2 - 1))

    lines = solver.answer_str.splitlines()
    for idx, line in enumerate(lines, 1):
        typer.echo(line, nl=False)

        if idx != len(lines):
            input()
        else:
            typer.echo()
