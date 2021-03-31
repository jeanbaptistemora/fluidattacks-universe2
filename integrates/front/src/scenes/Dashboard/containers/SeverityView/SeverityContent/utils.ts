import type { ISeverityAttr } from "../types";
import _ from "lodash";
import {
  attackComplexityOptions,
  attackVectorOptions,
  availabilityImpactOptions,
  confidentialityImpactOptions,
  exploitabilityOptions,
  integrityImpactOptions,
  remediationLevelOptions,
  reportConfidenceOptions,
  severityScopeOptions,
  userInteractionOptions,
} from "../utils";

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
    remediationLevel,
    reportConfidence,
    severityScope,
    userInteraction,
  } = severity;

  return (
    _.includes(Object.keys(attackVectorOptions), String(attackVector)) &&
    _.includes(
      Object.keys(attackComplexityOptions),
      String(attackComplexity)
    ) &&
    _.includes(
      Object.keys(availabilityImpactOptions),
      String(availabilityImpact)
    ) &&
    _.includes(
      Object.keys(confidentialityImpactOptions),
      String(confidentialityImpact)
    ) &&
    _.includes(Object.keys(exploitabilityOptions), String(exploitability)) &&
    _.includes(Object.keys(integrityImpactOptions), String(integrityImpact)) &&
    _.includes(
      Object.keys(remediationLevelOptions),
      String(remediationLevel)
    ) &&
    _.includes(
      Object.keys(reportConfidenceOptions),
      String(reportConfidence)
    ) &&
    _.includes(Object.keys(severityScopeOptions), String(severityScope)) &&
    _.includes(Object.keys(userInteractionOptions), String(userInteraction))
  );
}

export { validateValues };
