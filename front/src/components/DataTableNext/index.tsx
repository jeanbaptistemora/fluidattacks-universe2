/* tslint:disable: jsx-no-multiline-js variable-name
 * VARIABLE-NAME: Disabling here is necessary due a conflict
 * between lowerCamelCase var naming rule from tslint
 * and PascalCase rule for naming JSX elements
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code in graphql queries
 */
import _ from "lodash";
import React from "react";
/* tslint:disable-next-line:no-import-side-effect no-submodule-imports
* Disabling this two rules is necessary for
* allowing the import of default styles that ReactTable needs
* to display properly even if some of them are overridden later
*/
import "react-bootstrap-table-next/dist/react-bootstrap-table2.min.css";
// tslint:disable-next-line:no-import-side-effect no-submodule-imports
import "react-bootstrap-table2-paginator/dist/react-bootstrap-table2-paginator.min.css";
import ToolkitProvider, { ToolkitProviderProps } from "react-bootstrap-table2-toolkit";
// tslint:disable-next-line:no-import-side-effect no-submodule-imports
import "react-bootstrap-table2-toolkit/dist/react-bootstrap-table2-toolkit.min.css";
import { default as globalStyle } from "../../styles/global.css";
import { TableWrapper } from "./table";
import { ITableProps } from "./types";
import { customizeColumns } from "./utils";

const renderToolKitProvider: ((props: ITableProps, dataset: Array<{}>) => JSX.Element) =
  (props: ITableProps, dataset: Array<{}>): JSX.Element => {
    const { columnToggle, csvFilename = "spreadsheet.csv", search, title } = props;

    return (
      <div>
      {_.isEmpty(title) ? undefined : <h3 className={globalStyle.title}>{title}</h3>}
      <ToolkitProvider
        keyField={!_.isEmpty(dataset) && dataset.length > 0 ? "uniqueId" : "_"}
        data={dataset}
        columns={customizeColumns(props.headers, props.dataset, props.isFilterEnabled)}
        columnToggle={columnToggle}
        search={search}
        exportCSV={{
          fileName: csvFilename,
        }}
      >
        {(toolkitProps: ToolkitProviderProps): JSX.Element =>
          <TableWrapper toolkitProps={toolkitProps} tableProps={props} dataset={dataset}/>}
      </ToolkitProvider>
      </div>
    );
  };

export const dataTableNext: React.FunctionComponent<ITableProps> = (props: ITableProps): JSX.Element => {
  let dataset: Array<{}>;
  if (!_.isEmpty(props.dataset) && props.dataset.length > 0) {
    dataset = props.dataset.map((data: {uniqueId: number}, index: number) => {
      data.uniqueId = index;

      return data;
    });
  } else {
    dataset = [];
  }

  return (
    <React.StrictMode>
      <div id={props.id}>
        {_.isEmpty(dataset) && _.isEmpty(props.headers) ? <div/> : renderToolKitProvider(props, dataset)}
      </div>
    </React.StrictMode>
  );
};

export { dataTableNext as DataTableNext };
