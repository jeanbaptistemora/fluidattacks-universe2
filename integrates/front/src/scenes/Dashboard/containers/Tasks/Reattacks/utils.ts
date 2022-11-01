/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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
