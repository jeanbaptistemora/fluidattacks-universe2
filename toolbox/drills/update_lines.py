# Standard library
import csv
import os
import sys

# Local libraries
from toolbox.drills import (
    take_subscription_snapshot,
)

UNIQ = "----"
UNIQ_L = len(UNIQ)
FIELDS = [
    "filename",
    "loc",
    "tested-lines",
    "modified-date",
    "modified-commit",
    "tested-date",
    "comments"
]


def command(cmd: str):
    if os.system(cmd):
        raise Exception(f"CRITICAL: `{cmd}` return a non-zero status code.")


def sort_rows(path):
    command(f"(head -n 1 '{path}' && tail -n +2 '{path}' | LC_ALL=C sort) >"
            f"'{path}.{UNIQ}'")
    command(f"mv -f '{path}.{UNIQ}' '{path}'")


def remove_cr(path):
    command(f"tr -d '\r' < '{path}' > '{path}.{UNIQ}'")
    command(f"mv -f '{path}.{UNIQ}' '{path}'")


def append_changes(path):
    with open("toe/snapshot", "r") as snapshot, open(path, "a") as now:
        now_writer = csv.writer(now)
        for row in snapshot:
            modified_row = row.rsplit(",", 6)
            modified_row[0] += UNIQ
            modified_row[-1] = ""
            now_writer.writerow(modified_row)


def alter_state(path):
    command(f"mv '{path}' toe/lines.tmp")
    with open("toe/lines.tmp", "r") as now, \
            open(path, "w") as tmp:
        now_reader = csv.DictReader(now)
        tmp_writer = csv.DictWriter(tmp, fieldnames=FIELDS)
        tmp_writer.writeheader()
        state, cache = "init", None
        for row_now in now_reader:
            try:
                state, cache = alter_state__aux(row_now, state, cache,
                                                tmp_writer)
            except RuntimeError as exc:
                print(f"CRITICAL: File failed to update: {exc}")
                print(row_now)
                command("rm toe/lines.tmp toe/lines.stream")
                sys.exit()
    command("rm toe/lines.tmp")


def alter_state__aux(row, state, cache, writer):
    if state == "init":
        if row["filename"][-UNIQ_L:] == UNIQ:
            # new file
            row["filename"] = row["filename"][:-UNIQ_L]
            writer.writerow(row)
            state, cache = "init", None
        else:
            state, cache = "wait", row
    elif state == "wait":
        if row["filename"][-UNIQ_L:] == UNIQ:
            # merge new file (row) into old file (cache)
            if not cache["tested-date"]:
                cache["tested-date"] = "2000-01-01"
            if not cache["tested-lines"]:
                cache["tested-lines"] = 0
            if row["modified-commit"] != cache["modified-commit"]:
                row["filename"] = cache["filename"]
                row["tested-lines"] = 0
                row["tested-date"] = cache["tested-date"]
                row["comments"] = cache["comments"]
            else:
                row = cache
            writer.writerow(row)
            state, cache = "init", None
        else:
            # deleted file
            state, cache = alter_state__aux(row, "init", None, writer)
    return state, cache


def main(subs: str):
    init_dir: str = os.getcwd()

    try:
        os.chdir(f'subscriptions/{subs}')

        # We are going to operate over lines.stream until the end
        command("cp toe/lines.csv toe/lines.stream")
        # Create an snapshot of the current lines, dates, and hash
        take_subscription_snapshot.do_gen_stats()
        # Literraly dump the snapshot into the lines.stream creating duplicates
        append_changes("toe/lines.stream")
        # Clean up the snapshot
        command("rm toe/snapshot")
        # Remove carriage return and sort
        remove_cr("toe/lines.stream")
        sort_rows("toe/lines.stream")
        # Parse the duplicates
        alter_state("toe/lines.stream")
        # Remove carriage return and sort once again just to be sure
        remove_cr("toe/lines.stream")
        sort_rows("toe/lines.stream")
        # We are fine to go now
        command("mv -f toe/lines.stream toe/lines.csv")
    finally:
        os.chdir(init_dir)
