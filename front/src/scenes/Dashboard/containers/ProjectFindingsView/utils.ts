import { IFindingAttr } from "./types";
import _ from "lodash";
import { formatTreatment } from "../../../../utils/formatHelpers";
import translate from "../../../../utils/translations/translate";

export const formatFindings: (dataset: IFindingAttr[]) => IFindingAttr[] = (
  dataset: IFindingAttr[]
): IFindingAttr[] =>
  dataset.map((finding: IFindingAttr): IFindingAttr & {
    where: string;
  } => {
    const stateParameters: Record<string, string> = {
      closed: "search_findings.status.closed",
      open: "search_findings.status.open",
    };
    const typeParameters: Record<string, string> = {
      HYGIENE: "search_findings.tab_description.type.hygiene",
      SECURITY: "search_findings.tab_description.type.security",
    };
    const state: string = translate.t(stateParameters[finding.state]);
    const treatment: string = translate.t(
      formatTreatment(finding.treatment, finding.state)
    );
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
      .sort((a: string, b: string): number => a.localeCompare(b))
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
