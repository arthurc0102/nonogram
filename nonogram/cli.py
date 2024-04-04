import pathlib
import typing

import typer

from nonogram import services

app = typer.Typer()


@app.command()
def solve(file: typing.Annotated[pathlib.Path, typer.Argument()]) -> None:
    length, _, *info = file.read_text().splitlines()

    length = int(length)
    col_info = [[int(n) for n in i.split()] for i in info[:length]]
    row_info = [[int(n) for n in i.split()] for i in info[length + 1 :]]

    solver = services.NonogramSolver(col_info, row_info)
    typer.echo(solver.answer_str)
