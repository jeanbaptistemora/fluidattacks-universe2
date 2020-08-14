import { ITableProps } from "./types";
import React from "react";
import { TableWrapper } from "./table";
import _ from "lodash";
import { default as style } from "./index.css";
import ToolkitProvider, {
  ToolkitProviderProps,
} from "react-bootstrap-table2-toolkit";
import { addUniqueKeys, customizeColumns } from "./utils";
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
