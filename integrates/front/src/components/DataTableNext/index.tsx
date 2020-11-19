import type { ITableProps } from "components/DataTableNext/types";
import React from "react";
import { TableWrapper } from "components/DataTableNext/table";
import ToolkitProvider from "react-bootstrap-table2-toolkit";
import type { ToolkitProviderProps } from "react-bootstrap-table2-toolkit";
import _ from "lodash";
import style from "components/DataTableNext/index.css";
import {
  addUniqueKeys,
  customizeColumns,
} from "components/DataTableNext/utils";
import "react-bootstrap-table-next/dist/react-bootstrap-table2.min.css";
import "react-bootstrap-table2-paginator/dist/react-bootstrap-table2-paginator.min.css";
import "react-bootstrap-table2-toolkit/dist/react-bootstrap-table2-toolkit.min.css";

export const DataTableNext: React.FC<ITableProps> = (
  // Readonly utility type doesn't seem to work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
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

  const datasetWithUniqueKeys: Record<string, unknown>[] = !_.isEmpty(dataset)
    ? addUniqueKeys(dataset)
    : dataset;

  return (
    <div className={style.wFull} id={id}>
      {(!_.isEmpty(dataset) || !_.isEmpty(headers)) && (
        <ToolkitProvider
          columnToggle={columnToggle}
          columns={customizeColumns(headers, dataset, isFilterEnabled)}
          data={datasetWithUniqueKeys}
          exportCSV={{
            fileName: csvFilename,
          }}
          keyField={"uniqueId"}
          search={search}
        >
          {(
            // Readonly utility type doesn't work on deeply nested types
            // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
            toolkitProps: ToolkitProviderProps
          ): JSX.Element => (
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
