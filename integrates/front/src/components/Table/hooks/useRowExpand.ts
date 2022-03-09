import type { ExpandRowProps } from "react-bootstrap-table-next";

import { useStoredState } from "utils/hooks";

interface IRowExpandHandlers<T> {
  expandedRows: ExpandRowProps<T>["expanded"];
  handleRowExpand: ExpandRowProps<T>["onExpand"];
  handleRowExpandAll: ExpandRowProps<T>["onExpandAll"];
}

interface IRowExpandOptions<T> {
  storageKey: string;
  rows: T[];
  rowId: keyof T;
}

export const useRowExpand = <T>({
  rows,
  rowId,
  storageKey,
}: IRowExpandOptions<T>): IRowExpandHandlers<T> => {
  const [expandedIds, setExpandedIds] = useStoredState<string[]>(
    storageKey,
    [],
    sessionStorage
  );

  const getRowId = (row: T): string => String(row[rowId]);
  const allIds = rows.map(getRowId);
  const expandedRows = expandedIds.map((id): number => allIds.indexOf(id));

  const handleRowExpand = (row: T, isExpand: boolean): void => {
    setExpandedIds((currentValues): string[] => {
      if (isExpand) {
        return [...currentValues, getRowId(row)];
      }

      return currentValues.filter(
        (rootId): boolean => rootId !== getRowId(row)
      );
    });
  };

  const handleRowExpandAll = (isExpand: boolean): void => {
    if (isExpand) {
      setExpandedIds(allIds);
    } else {
      setExpandedIds([]);
    }
  };

  return { expandedRows, handleRowExpand, handleRowExpandAll };
};
