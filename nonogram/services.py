import enum
import itertools
import typing

from nonogram import exceptions


class NonogramSolver:
    class Status(enum.IntEnum):
        FILL = 1
        UNKNOWN = 0
        EMPTY = -1

    def __init__(self, col_info: list[list[int]], row_info: list[list[int]]) -> None:
        if len(col_info) != len(row_info):
            msg = "Col and Row length should be same"
            raise exceptions.NonogramError(msg)

        self.length = len(col_info)
        self.board = [[self.Status.UNKNOWN] * self.length for _ in range(self.length)]
        self.col_possibilities = [self.create_possibilities(c) for c in col_info]
        self.row_possibilities = [self.create_possibilities(r) for r in row_info]

    def create_possibilities(self, info: list[int]) -> list[list[Status]]:
        n_group = len(info)
        n_empty = self.length - sum(info) - n_group + 1

        possibilities: list[list[NonogramSolver.Status]] = []
        for c in itertools.combinations(range(n_group + n_empty), n_group):
            line: list[NonogramSolver.Status] = []
            for i in range(len(c)):
                pre = 0 if i == 0 else c[i - 1]
                for _ in range(c[i] - pre):
                    line.append(self.Status.EMPTY)

                line.extend([self.Status.FILL] * info[i])

            line.extend([self.Status.EMPTY] * (self.length - len(line)))
            possibilities.append(line)

        return possibilities

    def _fill_board(self, mode: typing.Literal["row", "col"]) -> None:
        if mode == "row":
            possibilities = self.row_possibilities
        else:
            possibilities = self.col_possibilities

        for p_idx, p in enumerate(possibilities):
            if len(p) == 1:
                for i in range(self.length):
                    if mode == "row":
                        self.board[p_idx][i] = p[0][i]
                    else:
                        self.board[i][p_idx] = p[0][i]

                continue

            for idx in range(self.length):
                for status in (self.Status.FILL, self.Status.EMPTY):
                    if not all(p[i][idx] == status for i in range(len(p))):
                        continue

                    if mode == "row":
                        self.board[p_idx][idx] = status
                    else:
                        self.board[idx][p_idx] = status

    def fill_row(self) -> None:
        self._fill_board("row")

    def fill_col(self) -> None:
        self._fill_board("col")

    def remove_impossible_possibilities(self) -> None:
        for row_idx, row in enumerate(self.board):
            for col_idx, col in enumerate(row):
                if col == self.Status.UNKNOWN:
                    continue

                for rp in self.row_possibilities[row_idx]:
                    if rp[col_idx] != col:
                        self.row_possibilities[row_idx].remove(rp)

                for cp in self.col_possibilities[col_idx]:
                    if cp[row_idx] != col:
                        self.col_possibilities[col_idx].remove(cp)

    @property
    def is_solved(self) -> bool:
        return self.Status.UNKNOWN not in itertools.chain.from_iterable(self.board)

    @property
    def answer(self) -> list[list[Status]]:
        while not self.is_solved:
            self.fill_row()
            self.remove_impossible_possibilities()

            self.fill_col()
            self.remove_impossible_possibilities()

        return self.board

    @property
    def answer_str(self) -> str:
        return "\n".join(
            "".join(("O" if c == self.Status.FILL else "X") for c in r)
            for r in self.answer
        )
