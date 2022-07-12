import _ from "lodash";

import type {
  IFindingFormatted,
  ITodoFindingToReattackAttr,
  IVulnerabilityEdge,
} from "scenes/Dashboard/containers/Tasks/Reattacks/types";

const getOldestRequestedReattackDate = (
  edges: IVulnerabilityEdge[]
): string => {
  const vulnsDates: string[] = edges.map(
    (vulnEdge: IVulnerabilityEdge): string =>
      vulnEdge.node.lastRequestedReattackDate
  );
  const minDate = _.min(vulnsDates);
  if (_.isUndefined(minDate)) {
    return "-";
  }

  return minDate;
};

const formatFindings = (
  findings: ITodoFindingToReattackAttr[]
): IFindingFormatted[] => {
  const formatted = findings.map(
    (finding): IFindingFormatted => ({
      ...finding,
      oldestReattackRequestedDate: getOldestRequestedReattackDate(
        finding.vulnerabilitiesToReattackConnection.edges
      ),
    })
  );

  return _.orderBy(formatted, ["oldestReattackRequestedDate"], ["asc"]);
};

export { formatFindings };
