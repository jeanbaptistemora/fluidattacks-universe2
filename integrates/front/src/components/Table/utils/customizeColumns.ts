import type { Property } from "csstype";
import _ from "lodash";
import type { CSSProperties } from "react";
import type { ColumnDescription, SortOrder } from "react-bootstrap-table-next";

import type { IHeaderConfig } from "components/Table/types";

interface IColumn extends ColumnDescription {
  onSort: (dataField: string, order: SortOrder) => void;
}

function defineWhitespace(
  wrapped: boolean | undefined,
  fallBack: Property.WhiteSpace
): Property.WhiteSpace | undefined {
  if (_.isUndefined(wrapped)) {
    return fallBack;
  }

  return wrapped ? "unset" : fallBack;
}

const addGivenHeaders = (
  headers: readonly Readonly<IHeaderConfig>[],
  isFilterEnabled: boolean = true
): IColumn[] =>
  headers.map((key: Readonly<IHeaderConfig>): IColumn => {
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
      csvExport: key.csvExport,
      dataField: key.dataField,
      filter: isFilterEnabled ? key.filter : undefined,
      formatExtraData: key,
      formatter: key.formatter,
      headerFormatter: key.headerFormatter,
      headerStyle: (): CSSProperties => ({
        whiteSpace: defineWhitespace(key.wrapped, "nowrap"),
        width: _.isUndefined(key.width) ? "auto" : key.width,
      }),
      hidden: _.isUndefined(key.visible) ? key.visible : !key.visible,
      onSort: handleSort,
      sort: true,
      sortFunc: key.sortFunc,
      style: (): CSSProperties => ({
        whiteSpace: defineWhitespace(key.wrapped, "pre-wrap"),
        wordBreak: _.isUndefined(key.wordBreak) ? "normal" : key.wordBreak,
      }),
      text: key.header,
      tooltipDataField: key.tooltipDataField,
    };
  });

const addDynamicHeaders = (
  dataFields: readonly string[]
): ColumnDescription[] => {
  const maxNumberOfFields: number = 10;
  const toManyFields: boolean = dataFields.length > maxNumberOfFields;

  return dataFields.map(
    (key: string): ColumnDescription => ({
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

export const customizeColumns = (
  headers: readonly Readonly<IHeaderConfig>[],
  dataset: readonly Readonly<Record<string, unknown>>[],
  isFilterEnabled?: boolean
): ColumnDescription[] =>
  _.isEmpty(headers)
    ? addDynamicHeaders(Object.keys(dataset[0]))
    : addGivenHeaders(headers, isFilterEnabled);
