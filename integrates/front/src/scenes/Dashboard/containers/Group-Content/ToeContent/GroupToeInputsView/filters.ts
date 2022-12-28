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
function filterDateRange<T extends Record<string, any>>(
  rows: T[],
  currentRange: { min: string; max: string },
  columnKey: string
): T[] {
  const selectedMinDate = new Date(currentRange.min);
  const selectedMaxDate = new Date(currentRange.max);

  return rows.filter((row: T): boolean => {
    const releaseDate = new Date(row[columnKey] as string);
    const minRange = _.isEmpty(currentRange.min)
      ? true
      : releaseDate >= selectedMinDate;
    const maxRange = _.isEmpty(currentRange.max)
      ? true
      : releaseDate <= selectedMaxDate;

    return minRange && maxRange;
  });
}

export { filterDateRange, filterSelect, filterSearchText };
