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

  return _.orderBy(formatted, ["oldestReattackRequestedDate"], ["asc"]);
};

export { formatFindings };
