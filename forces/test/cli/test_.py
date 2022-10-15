# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from click.testing import (
    CliRunner,
)
from forces.cli import (
    main,
)
import os


def test_cli_strict_no_breaking(test_token: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main, ["--token", test_token, "--strict", "--repo-name", "forces"]
    )
    assert result.exit_code == 1, result.exception


def test_cli_strict_breaking_low(test_token: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--token",
            test_token,
            "--strict",
            "--repo-name",
            "forces",
            "--breaking",
            "2",
        ],
    )
    assert result.exit_code == 1, result.exception


def test_cli_strict_breaking_high(test_token: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--token",
            test_token,
            "--strict",
            "--repo-name",
            "forces",
            "--breaking",
            "10",
        ],
    )
    assert result.exit_code == 0, result.exception


def test_cli_lax(test_token: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main, ["--token", test_token, "--lax", "--repo-path", "../"]
    )
    assert result.exit_code == 0, result.exception


def test_cli_invalid_group(test_token: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main, ["--token", test_token, "--lax", "--repo-path", "../"]
    )
    assert result.exit_code == 0, result.exception


def test_cli_out_to_file(test_token: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--token",
            test_token,
            "--strict",
            "--output",
            "test.yml",
            "--repo-path",
            "../",
        ],
    )
    assert os.path.exists(f"{os.getcwd()}/test.yml"), result.exception
