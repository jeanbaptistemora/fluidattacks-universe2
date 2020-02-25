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

export interface IExploitResult {
  kind: string;
  where: string;
  who: string;
}

export interface IFoundVulnerabilities {
  accepted: number;
  others: number;
  total: number;
}

export interface IVulnerabilities {
  acceptedExploits: IExploitResult[];
  exploits: IExploitResult[];
  mockedExploits: IExploitResult[];
  numOfVulnerabilitiesInAcceptedExploits: number;
  numOfVulnerabilitiesInExploits: number;
  numOfVulnerabilitiesInMockedExploits: number;
}

export interface IExecution {
  date: string;
  exitCode: string;
  foundVulnerabilities: IFoundVulnerabilities;
  gitRepo: string;
  identifier: string;
  kind: string;
  log: string;
  status: string;
  strictness: string;
  vulnerabilities: IVulnerabilities;
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
    // Warning: months are 0 indexed: January is 0, December is 11
    const month: string = toStringAndPad(dateObj.getMonth() + 1, 2);
    // Warning: Date.getDay() returns the day of the week: Monday is 1, Friday is 5
    const day: string = toStringAndPad(dateObj.getDate(), 2);
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
            const executions: IExecution[] = data.breakBuildExecutions.executions.map((execution: IExecution) => {
              const date: string = formatDate(execution.date);
              const kind: string = toTitleCase(execution.kind);
              const status: ReactElement = statusFormatter(execution.exitCode === "0" ? "Success" : "Failed");
              const strictness: string = toTitleCase(execution.strictness);
              const foundVulnerabilities: IFoundVulnerabilities = {
                accepted: execution.vulnerabilities.numOfVulnerabilitiesInAcceptedExploits,
                others: execution.vulnerabilities.numOfVulnerabilitiesInMockedExploits,
                total: execution.vulnerabilities.numOfVulnerabilitiesInExploits
                  + execution.vulnerabilities.numOfVulnerabilitiesInMockedExploits
                  + execution.vulnerabilities.numOfVulnerabilitiesInAcceptedExploits,
              };

              return {...execution, date, foundVulnerabilities, kind, status, strictness};
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
                  bsSize="large"
                  footer={<div />}
                  headerTitle={translate.t("project.forces.execution_details_modal.title")}
                  open={isExecutionDetailsModalOpen}
              >
              {currentRowIndex >= 0 && currentRowIndex < executions.length
                ? <div>
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
                    <Row>
                      <Col md={12}><p><b>{translate.t("project.forces.found_vulnerabilities.title")}</b></p></Col>
                    </Row>
                    <ul>
                      <li>
                        <p>
                          [{translate.t("project.forces.found_vulnerabilities.total")}]
                          &nbsp;{executions[currentRowIndex].foundVulnerabilities.total}
                        </p>
                      </li>
                      <li>
                        <p>
                          [{translate.t("project.forces.found_vulnerabilities.accepted")}]
                          &nbsp;{executions[currentRowIndex].foundVulnerabilities.accepted}
                        </p>
                      </li>
                      <li>
                        <p>
                          [{translate.t("project.forces.found_vulnerabilities.others")}]
                          &nbsp;{executions[currentRowIndex].foundVulnerabilities.others}
                        </p>
                      </li>
                    </ul>
                    <Row>
                      <Col md={12}><p><b>{translate.t("project.forces.tainted_toe.title")}</b></p></Col>
                    </Row>
                    <ul>
                      {executions[currentRowIndex].vulnerabilities.exploits.map(
                        (result: IExploitResult) => <li key={result.who}><p>[Security] {result.who}</p></li>)}
                      {executions[currentRowIndex].vulnerabilities.acceptedExploits.map(
                        (result: IExploitResult) => <li key={result.who}><p>[Accepted] {result.who}</p></li>)}
                      {executions[currentRowIndex].vulnerabilities.mockedExploits.map(
                        (result: IExploitResult) => <li key={result.who}><p>[Others] {result.who}</p></li>)}
                    </ul>
                    <hr />
                    <SyntaxHighlighter style={monokaiSublime} language="yaml" wrapLines={true}>
                      {executions[currentRowIndex].log}
                    </SyntaxHighlighter>
                    <ButtonToolbar className="pull-right">
                      <Button bsStyle="success" onClick={closeSeeExecutionDetailsModal}>
                        {translate.t("project.forces.execution_details_modal.close")}
                      </Button>
                    </ButtonToolbar>
                  </div>
                : "No data to display"}
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
