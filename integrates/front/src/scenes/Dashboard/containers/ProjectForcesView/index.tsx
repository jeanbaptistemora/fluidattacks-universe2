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
import { RouteComponentProps } from "react-router";
// tslint:disable-next-line no-submodule-imports
import SyntaxHighlighter from "react-syntax-highlighter/dist/esm/light";
// tslint:disable-next-line no-submodule-imports
import { default as monokaiSublime } from "react-syntax-highlighter/dist/esm/styles/hljs/monokai-sublime";

// Local imports
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import { Button } from "../../../../components/Button";
import { statusFormatter } from "../../../../components/DataTableNext/formatters";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeaderConfig } from "../../../../components/DataTableNext/types";
import { Modal } from "../../../../components/Modal";
import { Logger } from "../../../../utils/logger";
import { msgError } from "../../../../utils/notifications";
import { translate } from "../../../../utils/translations/translate";
import styles from "./index.css";
import { GET_FORCES_EXECUTIONS } from "./queries";

type ForcesViewProps = RouteComponentProps<{ projectName: string }>;

export interface IExploitResult {
  exploitability: number;
  kind: string;
  state: string;
  where: string;
  who: string;
}

export interface IFoundVulnerabilities {
  accepted: number;
  exploitable: number;
  notExploitable: number;
  total: number;
}

export interface IVulnerabilities {
  acceptedExploits: IExploitResult[];
  exploits: IExploitResult[];
  integratesExploits: IExploitResult[];
  numOfVulnerabilitiesInAcceptedExploits: number;
  numOfVulnerabilitiesInExploits: number;
  numOfVulnerabilitiesInIntegratesExploits: number;
}

export interface IExecution {
  date: string;
  execution_id: string;
  exitCode: string;
  foundVulnerabilities: IFoundVulnerabilities;
  gitRepo: string;
  kind: string;
  log: string;
  status: string;
  strictness: string;
  vulnerabilities: IVulnerabilities;
}

const projectForcesView: React.FunctionComponent<ForcesViewProps> = (props: ForcesViewProps): JSX.Element => {

  // States
  const defaultCurrentRow: IExecution = {
    date: "",
    execution_id: "",
    exitCode: "",
    foundVulnerabilities: {
      accepted: 0,
      exploitable: 0,
      notExploitable: 0,
      total: 0,
    },
    gitRepo: "",
    kind: "",
    log: "",
    status: "",
    strictness: "",
    vulnerabilities: {
      acceptedExploits: [],
      exploits: [],
      integratesExploits: [],
      numOfVulnerabilitiesInAcceptedExploits: 0,
      numOfVulnerabilitiesInExploits: 0,
      numOfVulnerabilitiesInIntegratesExploits: 0,
    },
  };
  const [currentRow, updateRow] = React.useState(defaultCurrentRow);
  const [isExecutionDetailsModalOpen, setExecutionDetailsModalOpen] = React.useState(false);

  const onSortState: ((dataField: string, order: SortOrder) => void) = (
    dataField: string, order: SortOrder,
  ): void => {
    const newSorted: Sorted = { dataField, order };
    sessionStorage.setItem("forcesSort", JSON.stringify(newSorted));
  };

  const toTitleCase: ((str: string) => string) = (str: string): string =>
    str.split(" ")
      .map((w: string): string => w[0].toUpperCase() + w.substr(1)
        .toLowerCase())
      .join(" ");

  const getVulnerabilitySummary:
    ((exploitable: number, accepted: number, notExploitable: number, total: number) => string) =
  (exploitable: number, accepted: number, notExploitable: number, total: number): string => {
    const exploitableTrans: string = translate.t("group.forces.found_vulnerabilities.exploitable");
    const acceptedTrans: string = translate.t("group.forces.found_vulnerabilities.accepted");
    const notExploitableTrans: string = translate.t("group.forces.found_vulnerabilities.not_exploitable");
    const totalTrans: string = translate.t("group.forces.found_vulnerabilities.total");

    const exploitableStr: string = `${exploitable} ${exploitableTrans}`;
    const acceptedStr: string = `${accepted} ${acceptedTrans}`;
    const notExploitableStr: string = `${notExploitable} ${notExploitableTrans}`;
    const totalStr: string = `${total} ${totalTrans}`;

    return `${exploitableStr}, ${acceptedStr}, ${notExploitableStr}, ${totalStr}`;
  };

  const stateResolve: (status: string) => string = (status: string): string => {
    switch (status) {
      case "OPEN":
        return translate.t("group.forces.status.vulnerable");
      case "CLOSED":
        return translate.t("group.forces.status.secure");
      case "ACCEPTED":
        return translate.t("group.forces.status.accepted");
      default:
        return "";
    }
  };

  const getDatasetFromVulnerabilities: ((vulnerabilities: IVulnerabilities) => Dictionary[]) = (
    vulnerabilities: IVulnerabilities,
  ): Dictionary[] => vulnerabilities.exploits.concat(
    vulnerabilities.acceptedExploits.concat(
      vulnerabilities.integratesExploits,
    ),
  )
    .map((elem: IExploitResult) => ({
      ...elem,
      state: statusFormatter(stateResolve(elem.state)),
    }));

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

  const formatText: ((text: string) => ReactElement<Text>) = (text: string): ReactElement<Text> =>
    <p className={styles.wrapped}>{text}</p>;

  const headersExecutionTable: IHeaderConfig[] = [
    {
      align: "center", dataField: "date", header: translate.t("group.forces.date"),
      onSort: onSortState, width: "13%",
    },
    {
      align: "center", dataField: "status", header: translate.t("group.forces.status.title"),
      onSort: onSortState, width: "13%", wrapped: true,
    },
    {
      align: "center", dataField: "foundVulnerabilities.total",
      header: translate.t("group.forces.status.vulnerabilities"),
      onSort: onSortState, width: "6%", wrapped: true,
    },
    {
      align: "center", dataField: "strictness", header: translate.t("group.forces.strictness.title"),
      onSort: onSortState, width: "5%", wrapped: true,
    },
    {
      align: "center", dataField: "kind", header: translate.t("group.forces.kind.title"),
      onSort: onSortState, width: "13%", wrapped: true,
    },
    {
      align: "center", dataField: "gitRepo", header: translate.t("group.forces.git_repo"),
      onSort: onSortState, width: "13%", wrapped: true,
    },
    {
      align: "center", dataField: "execution_id", header: translate.t("group.forces.identifier"),
      onSort: onSortState, width: "13%", wrapped: true,
    },
  ];
  const headersCompromisedToeTable: IHeaderConfig[] = [
    {
      dataField: "exploitability",
      formatter: formatText,
      header: translate.t("group.forces.compromised_toe.exploitability"),
      width: "15%",
      wrapped: true,
    },
    {
      dataField: "state",
      formatter: formatText,
      header: translate.t("group.forces.compromised_toe.status"),
      width: "10%",
      wrapped: true,
    },
    {
      dataField: "kind",
      formatter: formatText,
      header: translate.t("group.forces.compromised_toe.type"),
      width: "10%",
      wrapped: true,
    },
    {
      dataField: "who",
      formatter: formatText,
      header: translate.t("group.forces.compromised_toe.what"),
      wrapped: true,
    },
    {
      dataField: "where",
      formatter: formatText,
      header: translate.t("group.forces.compromised_toe.where"),
      wrapped: true,
    },
  ];
  const { projectName } = props.match.params;

  const openSeeExecutionDetailsModal: ((event: object, row: IExecution) => void) = (
    _0: object, row: IExecution,
  ): void => {
    updateRow(row);
    setExecutionDetailsModalOpen(true);
  };

  const closeSeeExecutionDetailsModal: (() => void) = (): void => {
    setExecutionDetailsModalOpen(false);
  };

  const handleQryErrors: ((error: ApolloError) => void) = (
    { graphQLErrors }: ApolloError,
  ): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(translate.t("group_alerts.error_textsad"));
      Logger.warning("An error occurred getting executions", error);
    });
  };

  return (
    <Query
      query={GET_FORCES_EXECUTIONS}
      variables={{ projectName }}
      onError={handleQryErrors}
    >
      {
        ({ data }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || _.isEmpty(data)) {
            return <React.Fragment />;
          }

          const executions: IExecution[] = data.forcesExecutions.executions.map((execution: IExecution) => {
              const date: string = formatDate(execution.date);
              const kind: string = toTitleCase(translate.t(
                execution.kind === "static" ? "group.forces.kind.static" : "group.forces.kind.dynamic"));
              const strictness: string = toTitleCase(translate.t(
                execution.strictness === "lax" ? "group.forces.strictness.tolerant" :
                "group.forces.strictness.strict"));
              const foundVulnerabilities: IFoundVulnerabilities = {
                accepted: execution.vulnerabilities.numOfVulnerabilitiesInAcceptedExploits,
                exploitable: execution.vulnerabilities.numOfVulnerabilitiesInExploits,
                notExploitable: execution.vulnerabilities.numOfVulnerabilitiesInIntegratesExploits,
                total: execution.vulnerabilities.numOfVulnerabilitiesInExploits
                  + execution.vulnerabilities.numOfVulnerabilitiesInIntegratesExploits
                  + execution.vulnerabilities.numOfVulnerabilitiesInAcceptedExploits,
              };
              const status: ReactElement = statusFormatter(translate.t(
                foundVulnerabilities.total === 0
                  ? "group.forces.status.secure"
                  : "group.forces.status.vulnerable"));

              return { ...execution, date, foundVulnerabilities, kind, status, strictness };
            });

          const initialSort: string = JSON.stringify({ dataField: "date", order: "desc" });

          return (
              <React.StrictMode>
                <p>{translate.t("group.forces.table_advice")}</p>
                <DataTableNext
                  bordered={true}
                  dataset={executions}
                  defaultSorted={JSON.parse(_.get(sessionStorage, "forcesSort", initialSort))}
                  exportCsv={true}
                  search={true}
                  headers={headersExecutionTable}
                  id="tblForcesExecutions"
                  pageSize={100}
                  rowEvents={{ onClick: openSeeExecutionDetailsModal }}
                />
              <Modal
                  bsSize="large"
                  footer={<div />}
                  headerTitle={translate.t("group.forces.execution_details_modal.title")}
                  open={isExecutionDetailsModalOpen}
                  onClose={closeSeeExecutionDetailsModal}
              >
                <div>
                  <Row>
                    <Col md={4}><p><b>{translate.t("group.forces.date")}</b></p></Col>
                    <Col md={8}><p>{currentRow.date}</p></Col>
                  </Row>
                  <Row>
                    <Col md={4}><p><b>{translate.t("group.forces.status.title")}</b></p></Col>
                    <Col md={8}><p>{currentRow.status}</p></Col>
                  </Row>
                  <Row>
                    <Col md={4}><p><b>{translate.t("group.forces.strictness.title")}</b></p></Col>
                    <Col md={8}><p>{currentRow.strictness}</p></Col>
                  </Row>
                  <Row>
                    <Col md={4}><p><b>{translate.t("group.forces.kind.title")}</b></p></Col>
                    <Col md={8}><p>{currentRow.kind}</p></Col>
                  </Row>
                  <Row>
                    <Col md={4}><p><b>{translate.t("group.forces.git_repo")}</b></p></Col>
                    <Col md={8}><p>{currentRow.gitRepo}</p></Col>
                  </Row>
                  <Row>
                    <Col md={4}><p><b>{translate.t("group.forces.identifier")}</b></p></Col>
                    <Col md={8}><p>{currentRow.execution_id}</p></Col>
                  </Row>
                  <Row>
                    <Col md={4}><p><b>{translate.t("group.forces.found_vulnerabilities.title")}</b></p></Col>
                    <Col md={8}>
                      <p className={styles.wrapped}>
                        {getVulnerabilitySummary(
                          currentRow.foundVulnerabilities.exploitable,
                          currentRow.foundVulnerabilities.accepted,
                          currentRow.foundVulnerabilities.notExploitable,
                          currentRow.foundVulnerabilities.total)}
                      </p>
                    </Col>
                  </Row>
                  <br />
                  <DataTableNext
                    bordered={true}
                    dataset={getDatasetFromVulnerabilities(currentRow.vulnerabilities)}
                    exportCsv={false}
                    search={false}
                    headers={headersCompromisedToeTable}
                    id="tblCompromisedToe"
                    pageSize={100}
                  />
                  <hr />
                  <SyntaxHighlighter style={monokaiSublime} language="yaml" wrapLines={true}>
                    {currentRow.log}
                  </SyntaxHighlighter>
                  <ButtonToolbar className="pull-right">
                    <Button bsStyle="success" onClick={closeSeeExecutionDetailsModal}>
                      {translate.t("group.forces.execution_details_modal.close")}
                    </Button>
                  </ButtonToolbar>
                </div>
              </Modal>
              </React.StrictMode>
            );
        }}
    </Query>
  );
};

export { projectForcesView as ProjectForcesView };
