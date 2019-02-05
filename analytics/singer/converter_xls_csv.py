#!/usr/bin/env python3

"""Minimalistic yet complete XLS to CSV converter."""

import csv
import argparse

import xlrd


def excel2csv(xls_file_path: str) -> None:
    """XLS to CSV converter."""
    workbook = xlrd.open_workbook(xls_file_path)
    for i in range(0, workbook.nsheets):
        sheet = workbook.sheet_by_index(i)
        with open(f"{sheet.name}.csv", "w") as file:
            print((
                f"Processing: {sheet.name} "
                f"[{sheet.ncols}c, {sheet.nrows}r]."))
            writer = csv.writer(
                file,
                delimiter=",",
                quotechar='"',
                quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow([cell.value for cell in sheet.row(0)])
            for row_idx in range(1, sheet.nrows):
                writer.writerow(
                    [
                        int(cell.value)
                        if isinstance(cell.value, float)
                        else cell.value
                        for cell in sheet.row(row_idx)
                    ])


def main():
    """Usual entry point."""
    # user interface
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "xls_file_path",
        help="XLS file path")
    args = parser.parse_args()

    excel2csv(args.xls_file_path)


if __name__ == "__main__":
    main()
