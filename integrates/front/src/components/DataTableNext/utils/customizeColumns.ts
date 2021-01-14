import type { Column } from "react-bootstrap-table-next";
import type { IHeaderConfig } from "components/DataTableNext/types";
import _ from "lodash";
import type { CSSProperties, ReactElement } from "react";

const handleFormatter: (
  value: string,
  row: Readonly<Record<string, string>>,
  rowIndex: number,
  key: Readonly<IHeaderConfig>
) => string | ReactElement | undefined = (
  value: string,
  row: Readonly<Record<string, string>>,
  rowIndex: number,
  key: Readonly<IHeaderConfig>
): string | ReactElement | undefined => {
  if (!_.isUndefined(key.formatter)) {
    return key.formatter(value, row, rowIndex, key);
  }
};

const addGivenHeaders: (
  headers: readonly Readonly<IHeaderConfig>[],
  isFilterEnabled?: boolean
) => Column[] = (
  headers: readonly Readonly<IHeaderConfig>[],
  isFilterEnabled: boolean = true
): Column[] =>
  headers.map(
    (key: Readonly<IHeaderConfig>): Column => {
      const handleSort: (dataField: string, order: SortOrder) => void = (
        dataField: string,
        order: SortOrder
      ): void => {
        if (!_.isUndefined(key.onSort)) {
          key.onSort(dataField, order);
        }
      };

      return {
        align: key.align,
        dataField: key.dataField,
        filter: isFilterEnabled ? key.filter : undefined,
        formatExtraData: key,
        formatter: _.isUndefined(key.formatter) ? undefined : handleFormatter,
        headerFormatter: key.headerFormatter,
        headerStyle: (): CSSProperties => ({
          whiteSpace: _.isUndefined(key.wrapped)
            ? "nowrap"
            : key.wrapped
            ? "unset"
            : "nowrap",
          width: _.isUndefined(key.width) ? "auto" : key.width,
        }),
        hidden: _.isUndefined(key.visible) ? key.visible : !key.visible,
        onSort: handleSort,
        sort: true,
        sortFunc: key.sortFunc,
        style: (): CSSProperties => ({
          whiteSpace: _.isUndefined(key.wrapped)
            ? "pre-wrap"
            : key.wrapped
            ? "unset"
            : "pre-wrap",
        }),
        text: key.header,
      };
    }
  );

const addDynamicHeaders: (dataFields: readonly string[]) => Column[] = (
  dataFields: readonly string[]
): Column[] => {
  const maxNumberOfFields: number = 10;
  const toManyFields: boolean = dataFields.length > maxNumberOfFields;

  return dataFields.map(
    (key: string): Column => ({
      dataField: key,
      headerStyle: (): CSSProperties => ({
        width: toManyFields ? "150px" : "auto",
      }),
      hidden: key === "uniqueId",
      sort: true,
      text: key,
    })
  );
};

export const customizeColumns: (
  headers: readonly Readonly<IHeaderConfig>[],
  dataset: readonly Readonly<Record<string, unknown>>[],
  isFilterEnabled?: boolean
) => Column[] = (
  headers: readonly Readonly<IHeaderConfig>[],
  dataset: readonly Readonly<Record<string, unknown>>[],
  isFilterEnabled?: boolean
): Column[] =>
  !_.isEmpty(headers)
    ? addGivenHeaders(headers, isFilterEnabled)
    : addDynamicHeaders(Object.keys(dataset[0]));
