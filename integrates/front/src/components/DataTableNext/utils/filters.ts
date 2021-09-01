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
      : selectedDate.getUTCDate() === reportDate.getDate() &&
          selectedDate.getUTCMonth() === reportDate.getMonth() &&
          selectedDate.getUTCFullYear() === reportDate.getFullYear();
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

export { filterDate, filterSelect, filterSearchText, filterText };
