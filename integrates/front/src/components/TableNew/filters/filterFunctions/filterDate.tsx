import type { Row, RowData } from "@tanstack/react-table";

export const filterDate = <TData extends RowData>(
  row: Row<TData>,
  columnId: string,
  filterValue: [number | undefined, number | undefined]
): boolean => {
  const currentDate = Date.parse(row.getValue(columnId));
  const isHigher =
    filterValue[0] === undefined ? true : currentDate >= filterValue[0];
  const isLower =
    filterValue[1] === undefined ? true : currentDate <= filterValue[1];

  return isHigher && isLower;
};
