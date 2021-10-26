from csv import (
    DictReader,
)
from datetime import (
    date,
    datetime,
)
from textwrap import (
    dedent,
)
from toolbox.logger import (
    LOGGER,
)
from toolbox.utils.function import (
    shield,
)


class Objective:
    # pylint: disable=too-few-public-methods
    def __init__(self, count: int, sofar: int, today: int) -> None:
        self.count = count
        self.sofar = sofar
        self.today = today


def process_lines_csv(subs: str) -> Objective:
    path: str = f"groups/{subs}/toe/lines.csv"
    date_format: str = "%Y-%m-%d"
    lines: Objective = Objective(count=0, sofar=0, today=0)
    try:
        with open(path, encoding="utf8") as lines_csv:
            for file in DictReader(lines_csv):
                lines.count += int(file["loc"])
                if file["tested-date"]:
                    tested_date: date = datetime.strptime(
                        file["tested-date"], date_format
                    ).date()
                    if tested_date <= date.today():
                        lines.sofar += int(file["tested-lines"])
                        if tested_date == date.today():
                            lines.today += int(file["tested-lines"])
    except FileNotFoundError as exc:
        LOGGER.warning("'%s' file not found.", exc.filename)
    return lines


def process_inputs_csv(subs: str) -> Objective:
    path: str = f"groups/{subs}/toe/inputs.csv"
    date_format: str = "%Y-%m-%d"
    inputs: Objective = Objective(count=0, sofar=0, today=0)
    try:
        with open(path, encoding="utf8") as inputs_csv:
            for file in DictReader(inputs_csv):
                if file["entry_point"]:
                    inputs.count += 1
                    if file["verified"] == "Yes" and file["tested_date"]:
                        tested_date: date = datetime.strptime(
                            file["tested_date"], date_format
                        ).date()
                        if tested_date <= date.today():
                            inputs.sofar += 1
                            if tested_date == date.today():
                                inputs.today += 1
    except FileNotFoundError as exc:
        LOGGER.warning("'%s' file not found.", exc.filename)
    return inputs


def safe_divide(num: float, den: float) -> float:
    if den == 0:
        return 1.0 if num == 0 else 0.0

    return num / den


def get_toe_coverage(lines: Objective, inputs: Objective) -> float:
    lines_per_target: int = 1000
    inputs_per_target: int = 2
    targets_per_line: float = 1 / lines_per_target
    targets_per_input: float = 1 / inputs_per_target

    toe_coverage: float = 100.0 * safe_divide(
        lines.sofar * targets_per_line + inputs.sofar * targets_per_input,
        lines.count * targets_per_line + inputs.count * targets_per_input,
    )
    return toe_coverage


def get_scope(lines: Objective, inputs: Objective) -> str:
    scope: str
    if lines.today > 0 and inputs.today > 0:
        scope = "cross"
    elif lines.today > 0 and inputs.today == 0:
        scope = "lines"
    elif inputs.today > 0 and lines.today == 0:
        scope = "inputs"
    else:
        scope = "cross"
        LOGGER.info("You may want to test the ToE before making the commit.")
    return scope


@shield(on_error_return=False)
def main(subs: str) -> bool:
    lines: Objective = process_lines_csv(subs)
    inputs: Objective = process_inputs_csv(subs)

    scope: str = get_scope(lines, inputs)
    cvrg: float = get_toe_coverage(lines, inputs)

    commit_msg: str = dedent(
        f"""    Commit Message:

    drills({scope}): {subs} - {cvrg:0.2f}%, {lines.today} el, {inputs.today} ei

    - {lines.sofar} el, {inputs.sofar} ei
    - {lines.count} vl, {inputs.count} vi
    - {cvrg:0.2f}% Total coverage
    """
    )

    if scope != "cross":
        if inputs.count == 0:
            commit_msg += dedent(
                """
            not-drills(cross)-because: toe-has-lines-only
            """
            )
        elif lines.count == lines.sofar:
            commit_msg += dedent(
                """
            not-drills(cross)-because: i-already-tested-all-lines
            """
            )
        elif inputs.count == inputs.sofar:
            commit_msg += dedent(
                """
            not-drills(cross)-because: i-already-tested-all-inputs
            """
            )
        else:
            commit_msg += dedent(
                """
            not-drills(cross)-because: <EXPLAIN HERE>
            """
            )

    LOGGER.info(commit_msg)

    LOGGER.info("Pending to test {%i - %i} lines.", lines.count, lines.sofar)
    LOGGER.info(
        "Pending to test {%i - %i} inputs.", inputs.count, inputs.sofar
    )

    return True
