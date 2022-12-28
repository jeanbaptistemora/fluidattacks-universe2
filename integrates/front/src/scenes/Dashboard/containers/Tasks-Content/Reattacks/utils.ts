import _ from "lodash";

import type {
  IFindingFormatted,
  ITodoFindingToReattackAttr,
  IVulnerabilityEdge,
} from "scenes/Dashboard/containers/Tasks-Content/Reattacks/types";

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

const noDate = (finding: IFindingFormatted): IFindingFormatted | undefined => {
  return finding.oldestReattackRequestedDate === "-" ? undefined : finding;
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
      url: `https://app.fluidattacks.com/groups/${finding.groupName}/vulns/${finding.id}/locations`,
    })
  );

  const fmtd = formatted.filter(noDate);

  return _.orderBy(fmtd, ["oldestReattackRequestedDate"], ["asc"]);
};

export { formatFindings };
