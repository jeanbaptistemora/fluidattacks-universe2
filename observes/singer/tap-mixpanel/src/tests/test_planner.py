import datetime
import pandas
import pytest
from tap_mixpanel import (
    planner,
)

Timestamp = pandas.Timestamp
DateOffset = pandas.DateOffset

strptime = datetime.datetime.strptime


@pytest.mark.freeze_time("2017-05-01")
def test_target_dates_month_start() -> None:
    # Arrange
    today = Timestamp(datetime.date.today())
    a_year_ago = today - DateOffset(days=365)
    # Act
    target_dates = planner.target_dates(a_year_ago)
    # Assert
    assert any(target_dates.previous_ranges.contains(today)) is False
    assert target_dates.actual_range and today in target_dates.actual_range


@pytest.mark.freeze_time("2017-05-15")
def test_target_dates_middle_date() -> None:
    # Arrange
    today = Timestamp(datetime.date.today())
    a_year_ago = today - DateOffset(days=365)
    # Act
    target_dates = planner.target_dates(a_year_ago)
    # Assert
    assert any(target_dates.previous_ranges.contains(today)) is False
    assert target_dates.actual_range and today in target_dates.actual_range


@pytest.mark.freeze_time("2017-05-31")
def test_target_dates_month_end() -> None:
    # Arrange
    today = Timestamp(datetime.date.today())
    a_year_ago = today - DateOffset(days=365)
    # Act
    target_dates = planner.target_dates(a_year_ago)
    # Assert
    assert any(target_dates.previous_ranges.contains(today)) is True
    assert target_dates.actual_range is None
