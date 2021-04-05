import _ from "lodash";

import { getLastTreatment } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import type { IFindingAttr } from "scenes/Dashboard/containers/ProjectFindingsView/types";
import { translate } from "utils/translations/translate";

const formatTreatmentSummary: (
  vulns: IFindingAttr["vulnerabilities"]
) => string = (vulns: IFindingAttr["vulnerabilities"]): string => {
  const zeroRisk: IFindingAttr["vulnerabilities"] = vulns.filter(
    (vuln: IFindingAttr["vulnerabilities"][0]): boolean => {
      return !["Confirmed", "Requested"].includes(vuln.zeroRisk);
    }
  );
  const lastTreatments: IHistoricTreatment[] = zeroRisk.map(
    (vuln: IFindingAttr["vulnerabilities"][0]): IHistoricTreatment =>
      getLastTreatment(vuln.historicTreatment)
  );
  const inProgress: number = lastTreatments.filter(
    (treatment: IHistoricTreatment): boolean =>
      treatment.treatment === "IN_PROGRESS"
  ).length;
  const temporarilyAccepted: number = lastTreatments.filter(
    (treatment: IHistoricTreatment): boolean =>
      treatment.treatment === "ACCEPTED"
  ).length;
  const indefinitelyAccepted: number = lastTreatments.filter(
    (treatment: IHistoricTreatment): boolean =>
      treatment.treatment === "ACCEPTED_UNDEFINED"
  ).length;

  return `
    ${translate.t("searchFindings.tabDescription.treatment.new")}: ${
    lastTreatments.length -
    inProgress -
    temporarilyAccepted -
    indefinitelyAccepted
  },
    ${translate.t(
      "searchFindings.tabDescription.treatment.inProgress"
    )}: ${inProgress},
    ${translate.t(
      "searchFindings.tabDescription.treatment.accepted"
    )}: ${temporarilyAccepted},
    ${translate.t(
      "searchFindings.tabDescription.treatment.acceptedUndefined"
    )}: ${indefinitelyAccepted}
  `;
};

const formatFindings: (dataset: IFindingAttr[]) => IFindingAttr[] = (
  dataset: IFindingAttr[]
): IFindingAttr[] =>
  dataset.map((finding: IFindingAttr): IFindingAttr & {
    where: string;
  } => {
    const stateParameters: Record<string, string> = {
      closed: "searchFindings.status.closed",
      open: "searchFindings.status.open",
    };
    const typeParameters: Record<string, string> = {
      HYGIENE: "searchFindings.tabDescription.type.hygiene",
      SECURITY: "searchFindings.tabDescription.type.security",
    };
    const state: string = translate.t(stateParameters[finding.state]);
    const treatment: string =
      finding.state === "open"
        ? formatTreatmentSummary(finding.vulnerabilities)
        : "-";
    const type: string = translate.t(typeParameters[finding.type]);
    const isExploitable: string = translate.t(
      finding.isExploitable
        ? "group.findings.boolean.True"
        : "group.findings.boolean.False"
    );
    const remediated: string = translate.t(
      Boolean(finding.remediated) || !finding.verified
        ? "group.findings.remediated.True"
        : "group.findings.remediated.False"
    );
    // Sort is actually mutating a copy created by map.
    // eslint-disable-next-line fp/no-mutating-methods
    const where: string = _.uniqBy(finding.vulnerabilities, "where")
      .map((vuln: { where: string }): string => vuln.where)
      .sort((valA: string, valB: string): number => valA.localeCompare(valB))
      .join(", ");

    return {
      ...finding,
      isExploitable,
      remediated,
      state,
      treatment,
      type,
      where,
    };
  });

export { formatFindings };
