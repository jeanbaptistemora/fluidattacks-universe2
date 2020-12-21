import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import _ from "lodash";
import { formatDropdownField } from "utils/formatHelpers";
import { getLastTreatment } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";
import { translate } from "utils/translations/translate";

const formatVulnerabilities: (
  vulnerabilities: IVulnRowAttr[]
) => IVulnRowAttr[] = (vulnerabilities: IVulnRowAttr[]): IVulnRowAttr[] =>
  vulnerabilities.map(
    (vulnerability: IVulnRowAttr): IVulnRowAttr => {
      const hasVulnCycles: boolean = _.toInteger(vulnerability.cycles) > 0;
      const lastTreatment: IHistoricTreatment = getLastTreatment(
        vulnerability.historicTreatment
      );
      const isPendingToApproval: boolean =
        lastTreatment.treatment === "ACCEPTED_UNDEFINED" &&
        lastTreatment.acceptanceStatus !== "APPROVED";
      const isVulnOpen: boolean = vulnerability.currentState === "open";
      const treatmentLabel: string =
        translate.t(formatDropdownField(lastTreatment.treatment)) +
        (isPendingToApproval
          ? translate.t(
              "search_findings.tab_description.treatment.pending_approval"
            )
          : "");

      return {
        ...vulnerability,
        cycles: hasVulnCycles ? vulnerability.cycles : "",
        efficacy: hasVulnCycles ? `${vulnerability.efficacy}%` : "",
        treatment: isVulnOpen ? treatmentLabel : "-",
        treatmentManager: isVulnOpen
          ? (lastTreatment.treatmentManager as string)
          : "-",
        verification:
          vulnerability.verification === "Verified"
            ? `${vulnerability.verification} (${vulnerability.currentState})`
            : vulnerability.verification,
      };
    }
  );

export { formatVulnerabilities };
