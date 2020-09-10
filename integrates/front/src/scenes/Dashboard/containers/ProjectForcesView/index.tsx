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
import { Execution } from "./execution";
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

export interface IFoundVulnerabilitiesNew {
  accepted: number;
  closed: number;
  open: number;
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

export interface IVulnerabilitiesNew {
  accepted: IExploitResult[];
  closed: IExploitResult[];
  numOfAcceptedVulnerabilities: number;
  numOfClosedVulnerabilities: number;
  numOfOpenVulnerabilities: number;
  open: IExploitResult[];
}

export interface IExecution {
  date: string;
  execution_id: string;
  exitCode: string;
  foundVulnerabilities: IFoundVulnerabilities | IFoundVulnerabilitiesNew;
  gitRepo: string;
  kind: string;
  log?: string;
  projectName?: string;
  status: string;
  strictness: string;
  vulnerabilities: IVulnerabilities | IVulnerabilitiesNew;
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

  const headersExecutionTable: IHeaderConfig[] = [
    {
      align: "center", dataField: "date", header: translate.t("group.forces.date"),
      onSort: onSortState,
    },
    {
      align: "center", dataField: "status", formatter: statusFormatter,
      header: translate.t("group.forces.status.title"), onSort: onSortState, wrapped: true,
    },
    {
      align: "center", dataField: "foundVulnerabilities.total",
      header: translate.t("group.forces.status.vulnerabilities"),
      onSort: onSortState, wrapped: true,
    },
    {
      align: "center", dataField: "strictness", header: translate.t("group.forces.strictness.title"),
      onSort: onSortState, wrapped: true,
    },
    {
      align: "center", dataField: "kind", header: translate.t("group.forces.kind.title"),
      onSort: onSortState,  wrapped: true,
    },
    {
      align: "center", dataField: "gitRepo", header: translate.t("group.forces.git_repo"),
      onSort: onSortState, wrapped: true,
    },
    {
      align: "center", dataField: "execution_id", header: translate.t("group.forces.identifier"),
      onSort: onSortState, wrapped: true,
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

          const executions: IExecution[] = data.forcesExecutions.executions
            .concat(data.forcesExecutionsNew.executions)
            .map((execution: IExecution) => {
              const date: string = formatDate(execution.date);
              const kind: string = toTitleCase(
                translate.t(
                  execution.kind === "static"
                    ? "group.forces.kind.static"
                    : "group.forces.kind.dynamic"));
              const strictness: string = toTitleCase(
                translate.t(
                  execution.strictness === "lax"
                    ? "group.forces.strictness.tolerant"
                    : "group.forces.strictness.strict"));
              const vulnerabilities: IVulnerabilities | IVulnerabilitiesNew =
                execution.vulnerabilities;
              const foundVulnerabilities:
                | IFoundVulnerabilitiesNew
                | IFoundVulnerabilities =
                "numOfAcceptedVulnerabilities" in vulnerabilities
                  ? {
                    accepted: vulnerabilities.numOfAcceptedVulnerabilities,
                    closed: vulnerabilities.numOfClosedVulnerabilities,
                    open: vulnerabilities.numOfOpenVulnerabilities,
                    total:
                      vulnerabilities.numOfAcceptedVulnerabilities +
                      vulnerabilities.numOfOpenVulnerabilities +
                      vulnerabilities.numOfClosedVulnerabilities,
                  }
                  : {
                    accepted:
                      vulnerabilities.numOfVulnerabilitiesInAcceptedExploits,
                    exploitable:
                      vulnerabilities.numOfVulnerabilitiesInExploits,
                    notExploitable:
                      vulnerabilities.numOfVulnerabilitiesInIntegratesExploits,
                    total:
                      vulnerabilities.numOfVulnerabilitiesInExploits +
                      vulnerabilities.numOfVulnerabilitiesInIntegratesExploits +
                      vulnerabilities.numOfVulnerabilitiesInAcceptedExploits,
                  };
              const status: string = translate.t(
                foundVulnerabilities.total === 0
                  ? "group.forces.status.secure"
                  : "group.forces.status.vulnerable");

              return {
                ...execution,
                date,
                foundVulnerabilities,
                kind,
                status,
                strictness,
              };
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
                <Execution {...currentRow} />
                <ButtonToolbar className="pull-right">
                  <Button bsStyle="success" onClick={closeSeeExecutionDetailsModal}>
                    {translate.t("group.forces.execution_details_modal.close")}
                  </Button>
                </ButtonToolbar>
              </Modal>
              </React.StrictMode>
            );
        }}
    </Query>
  );
};

export { projectForcesView as ProjectForcesView };
