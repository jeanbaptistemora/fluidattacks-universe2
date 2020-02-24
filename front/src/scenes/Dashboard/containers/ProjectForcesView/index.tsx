/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for the sake of readability
 */

// Third parties imports
import { QueryResult } from "@apollo/react-common";
import { Query } from "@apollo/react-components";
import _ from "lodash";
import React, { ReactElement } from "react";
import { ButtonToolbar, Col, Row } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { RouteComponentProps } from "react-router";
// tslint:disable-next-line no-submodule-imports
import SyntaxHighlighter from "react-syntax-highlighter/dist/esm/light";
// tslint:disable-next-line no-submodule-imports
import { default as monokaiSublime } from "react-syntax-highlighter/dist/esm/styles/hljs/monokai-sublime";
import { Dispatch } from "redux";

// Local imports
import { Button } from "../../../../components/Button";
import { statusFormatter } from "../../../../components/DataTableNext/formatters";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeader } from "../../../../components/DataTableNext/types";
import { Modal } from "../../../../components/Modal";
import { handleGraphQLErrors } from "../../../../utils/formatHelpers";
import translate from "../../../../utils/translations/translate";
import { IDashboardState } from "../../reducer";
import { changeSortValues } from "./actions";
import { GET_FORCES_EXECUTIONS } from "./queries";

type ForcesViewProps = RouteComponentProps<{ projectName: string }>;

export interface IExecution {
  date: string;
  exitCode: string;
  gitRepo: string;
  identifier: string;
  kind: string;
  status: string;
  strictness: string;
}

const projectForcesView: React.FunctionComponent<ForcesViewProps> = (props: ForcesViewProps): JSX.Element => {

  interface IState { dashboard: IDashboardState; }
  const forces: IDashboardState["forces"] = useSelector(
    (state: IState): IDashboardState["forces"] => state.dashboard.forces);

  // States
  const [currentRowIndex, updateRowIndex] = React.useState(0);
  const [sortValue, setSortValue] = React.useState(forces.defaultSort);
  const [isExecutionDetailsModalOpen, setExecutionDetailsModalOpen] = React.useState(false);

  const dispatch: Dispatch = useDispatch();

  const onSortState: ((dataField: string, order: SortOrder) => void) =
  (dataField: string, order: SortOrder): void => {
    const newSorted: Sorted = {dataField,  order};
    if (!_.isEqual(newSorted, sortValue)) {
      setSortValue(newSorted);
      dispatch(changeSortValues(newSorted));
    }
  };

  const toTitleCase: ((str: string) => string) = (str: string): string =>
    str.split(" ")
        .map((w: string): string => w[0].toUpperCase() + w.substr(1)
                                                          .toLowerCase())
        .join(" ");

  const formatDate: ((date: string) => string) = (date: string): string => {
    const dateObj: Date = new Date(date);

    const toStringAndPad: ((input: number, positions: number) => string) =
    (input: number, positions: number): string => input.toString()
                                                       .padStart(positions, "0");

    const year: string = toStringAndPad(dateObj.getFullYear(), 4);
    const month: string = toStringAndPad(dateObj.getMonth(), 2);
    const day: string = toStringAndPad(dateObj.getDay(), 2);
    const hours: string = toStringAndPad(dateObj.getHours(), 2);
    const minutes: string = toStringAndPad(dateObj.getMinutes(), 2);

    return `${year}-${month}-${day} ${hours}:${minutes}`;
  };

  const tableHeaders: IHeader[] = [
    {
      align: "center", dataField: "date", header: translate.t("project.forces.date"),
      onSort: onSortState, width: "13%", wrapped: true,
    },
    {
      align: "center", dataField: "status", header: translate.t("project.forces.status"),
      onSort: onSortState, width: "13%", wrapped: true,
    },
    {
      align: "center", dataField: "strictness", header: translate.t("project.forces.strictness"),
      onSort: onSortState, width: "5%", wrapped: true,
    },
    {
      align: "center", dataField: "kind", header: translate.t("project.forces.kind"),
      onSort: onSortState, width: "5%", wrapped: true,
    },
    {
      align: "center", dataField: "gitRepo", header: translate.t("project.forces.git_repo"),
      onSort: onSortState, width: "13%", wrapped: true,
    },
    {
      align: "center", dataField: "identifier", header: translate.t("project.forces.identifier"),
      onSort: onSortState, width: "13%", wrapped: true,
    },
  ];
  const { projectName } = props.match.params;

  const openSeeExecutionDetailsModal: ((event: object, row: object, rowIndex: number) => void) =
  (event: object, row: object, rowIndex: number): void => {
    updateRowIndex(rowIndex);
    setExecutionDetailsModalOpen(true);
  };

  const closeSeeExecutionDetailsModal: (() => void) = (): void => {
    setExecutionDetailsModalOpen(false);
  };

  return (
    <Query
      query={GET_FORCES_EXECUTIONS}
      variables={{ projectName }}
    >
      {
        ({ data, error, refetch }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || _.isEmpty(data)) {
            return <React.Fragment />;
          }
          if (!_.isUndefined(error)) {
            handleGraphQLErrors("An error occurred getting executions", error);

            return <React.Fragment />;
          }
          if (!_.isUndefined(data)) {
            const executions: Dictionary[] = data.breakBuildExecutions.executions.map((execution: IExecution) => {
              const date: string = formatDate(execution.date);
              const kind: string = toTitleCase(execution.kind);
              const status: ReactElement = statusFormatter(execution.exitCode === "0" ? "Success" : "Failed");
              const strictness: string = toTitleCase(execution.strictness);

              return {...execution, date, kind, status, strictness};
            });

            return (
              <React.StrictMode>
                <p>{translate.t("project.forces.table_advice")}</p>
                <DataTableNext
                  bordered={true}
                  dataset={executions}
                  defaultSorted={sortValue}
                  exportCsv={true}
                  search={true}
                  headers={tableHeaders}
                  id="tblForcesExecutions"
                  pageSize={100}
                  remote={false}
                  rowEvents={{onClick: openSeeExecutionDetailsModal}}
                  title=""
                />
              <Modal
                  footer={<div />}
                  headerTitle={translate.t("project.forces.execution_details_modal.title")}
                  open={isExecutionDetailsModalOpen}
              >
                <hr />
                <Row>
                  <Col md={4}><p><b>{translate.t("project.forces.date")}</b></p></Col>
                  <Col md={8}><p>{executions[currentRowIndex].date}</p></Col>
                </Row>
                <Row>
                  <Col md={4}><p><b>{translate.t("project.forces.status")}</b></p></Col>
                  <Col md={8}><p>{executions[currentRowIndex].status}</p></Col>
                </Row>
                <Row>
                  <Col md={4}><p><b>{translate.t("project.forces.strictness")}</b></p></Col>
                  <Col md={8}><p>{executions[currentRowIndex].strictness}</p></Col>
                </Row>
                <Row>
                  <Col md={4}><p><b>{translate.t("project.forces.kind")}</b></p></Col>
                  <Col md={8}><p>{executions[currentRowIndex].kind}</p></Col>
                </Row>
                <Row>
                  <Col md={4}><p><b>{translate.t("project.forces.git_repo")}</b></p></Col>
                  <Col md={8}><p>{executions[currentRowIndex].gitRepo}</p></Col>
                </Row>
                <Row>
                  <Col md={4}><p><b>{translate.t("project.forces.identifier")}</b></p></Col>
                  <Col md={8}><p>{executions[currentRowIndex].identifier}</p></Col>
                </Row>
                <hr />
                <SyntaxHighlighter style={monokaiSublime} language="yaml" wrapLines={true}>
                  {currentRowIndex >= 0 && currentRowIndex < executions.length
                    ? executions[currentRowIndex].log
                    : "Unable to retrieve"}
                </SyntaxHighlighter>
                <ButtonToolbar className="pull-right">
                  <Button bsStyle="success" onClick={closeSeeExecutionDetailsModal}>
                    {translate.t("project.forces.execution_details_modal.close")}
                  </Button>
                </ButtonToolbar>
              </Modal>
              </React.StrictMode>
            );
          } else {
            return <React.Fragment />;
          }
        }}
    </Query>
  );
};

export { projectForcesView as ProjectForcesView };
