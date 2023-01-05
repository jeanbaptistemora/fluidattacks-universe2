import _ from "lodash";

import type {
  IExecution,
  IFoundVulnerabilities,
  IVulnerabilities,
} from "scenes/Dashboard/containers/Group-Content/GroupForcesView/types";
import { formatDate } from "utils/formatHelpers";
import { translate } from "utils/translations/translate";

const toTitleCase: (str: string) => string = (str: string): string =>
  str
    .split(" ")
    .map(
      (item: string): string =>
        item[0].toUpperCase() + item.slice(1).toLowerCase()
    )
    .join(" ");

const formatFoundVulnerabilities: (
  vulnerabilities: IVulnerabilities
) => IFoundVulnerabilities = (
  vulnerabilities: IVulnerabilities
): IFoundVulnerabilities => {
  return {
    accepted: vulnerabilities.numOfAcceptedVulnerabilities,
    closed: vulnerabilities.numOfClosedVulnerabilities,
    open: vulnerabilities.numOfOpenVulnerabilities,
    total:
      vulnerabilities.numOfAcceptedVulnerabilities +
      vulnerabilities.numOfOpenVulnerabilities +
      vulnerabilities.numOfClosedVulnerabilities,
  };
};

const formatExecutions: (executions: { node: IExecution }[]) => IExecution[] = (
  executions: { node: IExecution }[]
): IExecution[] => {
  return executions.map((execution: { node: IExecution }): IExecution => {
    const date: string = formatDate(execution.node.date);
    const kind: string = translate.t(
      `group.forces.kind.${execution.node.kind.toLowerCase()}`
    );
    const strictness: string = toTitleCase(
      translate.t(
        execution.node.strictness === "lax"
          ? "group.forces.strictness.tolerant"
          : "group.forces.strictness.strict"
      )
    );
    const { vulnerabilities } = execution.node;
    const foundVulnerabilities: IFoundVulnerabilities = _.isNull(
      vulnerabilities
    )
      ? {
          accepted: 0,
          closed: 0,
          open: 0,
          total: 0,
        }
      : formatFoundVulnerabilities(vulnerabilities);
    const status: string = translate.t(
      foundVulnerabilities.open === 0
        ? "group.forces.status.secure"
        : "group.forces.status.vulnerable"
    );

    return {
      ...execution.node,
      date,
      foundVulnerabilities,
      kind,
      status,
      strictness,
    };
  });
};

const formatExecutionFilters: (state: string) => string = (
  state: string
): string => {
  const execFormat: Record<string, string> = {
    gitRepo: "gitRepo",
    kind: "type",
    status: "status",
    strictness: "strictness",
  };

  return execFormat[state];
};

export {
  toTitleCase,
  formatFoundVulnerabilities,
  formatExecutions,
  formatExecutionFilters,
};
