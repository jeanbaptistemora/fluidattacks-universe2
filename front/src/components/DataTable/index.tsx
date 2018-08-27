/* tslint:disable jsx-no-multiline-js
 * Disabling this rule is necessary for the sake of readability
 * of the code that dynamically creates the columns
 */
import PropTypes from "prop-types";
import React from "react";
import ReactTable, { ReactTableDefaults } from "react-table";
/* tslint:disable-next-line:no-import-side-effect no-submodule-imports
 * Disabling this two rules is necessary for
 * allowing the import of default styles that ReactTable needs
 * to display properly even if some of them are overridden later
 */
import "react-table/react-table.css";
import globalStyle from "../../styles/global.css";
import style from "./index.css";

interface ITableProps {
  /* tslint:disable-next-line:no-any
   * Disabling this rule is necessary because the dataset
   * array may contain different types since this is a
   * generic component
   */
  dataset: any[];
  title: string;
}

const dataTable: React.StatelessComponent<ITableProps> =
  (props: ITableProps): JSX.Element => (
    <React.StrictMode>
      <div>
        <h1 className={globalStyle.title}>{props.title}</h1>
        <ReactTable
          className="-striped -highlight"
          showPagination={props.dataset.length > 25}
          defaultPageSize={25}
          showPageSizeOptions={false}
          sortable={true}
          minRows={0}
          data={props.dataset}
          columns={
            Object.keys(props.dataset[0])
            .map((key: string) =>
              ({
                Header: key,
                accessor: key,
              }))
          }
          column={
            {
              ...ReactTableDefaults.column,
              className: style.td,
              headerClassName: style.th,
            }
          }
        />
      </div>
    </React.StrictMode>
  );

dataTable.propTypes = {
  dataset: PropTypes.any,
  title: PropTypes.string,
};

dataTable.defaultProps = {
  dataset: [{}],
};

export = dataTable;
