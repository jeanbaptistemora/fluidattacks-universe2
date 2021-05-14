import _ from "lodash";
import React from "react";
import type { SearchMatchProps } from "react-bootstrap-table2-toolkit";
import ToolkitProvider from "react-bootstrap-table2-toolkit";

import style from "components/DataTableNext/index.css";
import { TableWrapper } from "components/DataTableNext/table";
import type { ITableProps } from "components/DataTableNext/types";
import {
  addUniqueKeys,
  customizeColumns,
} from "components/DataTableNext/utils";
import "react-bootstrap-table-next/dist/react-bootstrap-table2.min.css";
import "react-bootstrap-table2-paginator/dist/react-bootstrap-table2-paginator.min.css";

export const DataTableNext: React.FC<ITableProps> = (
  props: ITableProps
): JSX.Element => {
  const {
    columnToggle = false,
    csvFilename = "spreadsheet.csv",
    dataset = [],
    headers,
    id,
    isFilterEnabled,
    search,
  } = props;

  const datasetWithUniqueKeys: Record<string, unknown>[] = _.isEmpty(dataset)
    ? dataset
    : addUniqueKeys(dataset);

  function onColumnMatch({ searchText, row }: SearchMatchProps): boolean {
    if (_.isEmpty(searchText)) {
      return true;
    }

    return _.some(row, (value: unknown): boolean =>
      _.isString(value)
        ? _.includes(value.toLowerCase(), searchText.toLowerCase())
        : false
    );
  }

  return (
    <div className={style.wFull} id={id}>
      {(!_.isEmpty(dataset) || !_.isEmpty(headers)) && (
        <ToolkitProvider
          columnToggle={columnToggle}
          columns={customizeColumns(headers, dataset, isFilterEnabled)}
          data={datasetWithUniqueKeys}
          exportCSV={{ fileName: csvFilename }}
          keyField={"uniqueId"}
          search={search ? { onColumnMatch } : undefined}
        >
          {(toolkitProps): JSX.Element => (
            <TableWrapper
              dataset={datasetWithUniqueKeys}
              tableProps={props}
              toolkitProps={toolkitProps}
            />
          )}
        </ToolkitProvider>
      )}
    </div>
  );
};
