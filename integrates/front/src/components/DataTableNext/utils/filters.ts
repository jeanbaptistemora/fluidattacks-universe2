/* eslint-disable @typescript-eslint/no-unsafe-member-access */
/* eslint-disable @typescript-eslint/no-unsafe-call */
import _ from "lodash";
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function filterSelect<T extends Record<string, any>>(
  rows: T[],
  currentValue: string,
  columnKey: string
): T[] {
  return rows.filter((row: T): boolean =>
    _.isEmpty(currentValue) ? true : row[columnKey] === currentValue
  );
}
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function filterText<T extends Record<string, any>>(
  rows: T[],
  searchText: string,
  columnKey: string
): T[] {
  return rows.filter((row: T): boolean =>
    _.isEmpty(searchText)
      ? true
      : _.includes(row[columnKey].toLowerCase(), searchText.toLowerCase())
  );
}
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function filterDate<T extends Record<string, any>>(
  rows: T[],
  currentDate: string,
  dateColumnKey: string
): T[] {
  const selectedDate = new Date(currentDate);

  return rows.filter((row: T): boolean => {
    const reportDate = new Date(row[dateColumnKey]);

    return _.isEmpty(currentDate)
      ? true
      : selectedDate.getUTCDate() === reportDate.getUTCDate() &&
          selectedDate.getUTCMonth() === reportDate.getUTCMonth() &&
          selectedDate.getUTCFullYear() === reportDate.getUTCFullYear();
  });
}
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function filterSearchText<T extends Record<string, any>>(
  rows: T[],
  searchText: string
): T[] {
  return rows.filter((row: T): boolean =>
    _.isEmpty(searchText)
      ? true
      : _.some(row, (value: unknown): boolean =>
          _.isString(value)
            ? _.includes(value.toLowerCase(), searchText.toLowerCase())
            : false
        )
  );
}
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function filterLastNumber<T extends Record<string, any>>(
  rows: T[],
  currentNumber: string,
  columnKey: string
): T[] {
  return rows.filter((row: T): boolean =>
    _.isEmpty(currentNumber)
      ? true
      : Number(row[columnKey]) <= Number(currentNumber)
  );
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function filterRange<T extends Record<string, any>>(
  rows: T[],
  currentRange: { min: string; max: string },
  columnKey: string
): T[] {
  return rows.filter((row: T): boolean => {
    const minRange = _.isEmpty(currentRange.min)
      ? true
      : Number(row[columnKey]) >= Number(currentRange.min);
    const maxRange = _.isEmpty(currentRange.max)
      ? true
      : Number(row[columnKey]) <= Number(currentRange.max);

    return minRange && maxRange;
  });
}

export {
  filterDate,
  filterLastNumber,
  filterRange,
  filterSelect,
  filterSearchText,
  filterText,
};
