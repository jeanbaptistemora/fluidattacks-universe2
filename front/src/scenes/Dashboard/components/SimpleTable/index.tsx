/* tslint:disable jsx-no-lambda no-any
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 */
import React from "react";
import { Col, Row } from "react-bootstrap";
import { dataTable as DataTable, ITableProps } from "../../../../components/DataTable/index";
import { default as style } from "./index.css";

const simpleTable: React.FunctionComponent<ITableProps> =
  (props: ITableProps): JSX.Element => (
  <React.StrictMode>
    <Row>
      <Col md={12} sm={12}>
        <DataTable
          tableHeader={style.tableHeader}
          tableBody={style.tableBody}
          tableContainer={style.tableContainer}
          dataset={props.dataset}
          onClickRow={(): void => undefined}
          enableRowSelection={props.enableRowSelection}
          exportCsv={props.exportCsv}
          headers={props.headers}
          id={props.id}
          pageSize={props.pageSize}
          striped={false}
          title={props.title}
          selectionMode={props.selectionMode}
        />
      </Col>
    </Row>
  </React.StrictMode>
);

simpleTable.defaultProps = {
  enableRowSelection: false,
  exportCsv: false,
  headers: [],
  onClickRow: (arg1: string): void => undefined,
  pageSize: 25,
  search: false,
};

export = simpleTable;
