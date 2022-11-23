import _ from "lodash";

import type { ISeverityAttr } from "../types";
import {
  attackComplexityOptions,
  attackVectorOptions,
  availabilityImpactOptions,
  castPrivileges,
  confidentialityImpactOptions,
  exploitabilityOptions,
  integrityImpactOptions,
  remediationLevelOptions,
  reportConfidenceOptions,
  severityScopeOptions,
  userInteractionOptions,
} from "../utils";

interface ISeverityValidation {
  value: string;
  options: Record<string, string>;
}
function validateValues(
  severity: ISeverityAttr["finding"]["severity"]
): boolean {
  const {
    attackComplexity,
    attackVector,
    availabilityImpact,
    confidentialityImpact,
    exploitability,
    integrityImpact,
    privilegesRequired,
    remediationLevel,
    reportConfidence,
    severityScope,
    userInteraction,
  } = severity;

  const optionsList: ISeverityValidation[] = [
    { options: attackComplexityOptions, value: attackComplexity },
    { options: attackVectorOptions, value: attackVector },
    { options: availabilityImpactOptions, value: availabilityImpact },
    { options: confidentialityImpactOptions, value: confidentialityImpact },
    { options: exploitabilityOptions, value: exploitability },
    { options: integrityImpactOptions, value: integrityImpact },
    { options: castPrivileges(severityScope), value: privilegesRequired },
    { options: remediationLevelOptions, value: remediationLevel },
    { options: reportConfidenceOptions, value: reportConfidence },
    { options: severityScopeOptions, value: severityScope },
    { options: userInteractionOptions, value: userInteraction },
  ];

  return _.every(
    _.map(optionsList, (optionsItem: ISeverityValidation): boolean =>
      _.includes(Object.keys(optionsItem.options), String(optionsItem.value))
    )
  );
}

export { validateValues };
