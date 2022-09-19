/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import _ from "lodash";

import type {
  IVulnFormatted,
  IVulnerabilityAttr,
} from "scenes/Dashboard/containers/Tasks/Reattacks/types";

const formatVulns = (nodes: IVulnerabilityAttr[]): IVulnFormatted[] => {
  const formatted = nodes.map(
    (vuln): IVulnFormatted => ({
      ...vuln,
      oldestReattackRequestedDate: vuln.lastRequestedReattackDate,
    })
  );

  return _.orderBy(formatted, ["oldestReattackRequestedDate"], ["asc"]);
};

export { formatVulns };
