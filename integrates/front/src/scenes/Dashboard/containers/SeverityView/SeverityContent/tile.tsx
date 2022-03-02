import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import { ReactSVG } from "react-svg";

import attackComplexityHigh from "resources/attackComplexityHigh.svg";
import attackComplexityLow from "resources/attackComplexityLow.svg";
import attackVectorAdjacent from "resources/attackVectorAdjacent.svg";
import attackVectorLocal from "resources/attackVectorLocal.svg";
import attackVectorNetwork from "resources/attackVectorNetwork.svg";
import attackVectorPhysical from "resources/attackVectorPhysical.svg";
import availabilityImpactHigh from "resources/availabilityImpactHigh.svg";
import availabilityImpactLow from "resources/availabilityImpactLow.svg";
import availabilityImpactNone from "resources/availabilityImpactNone.svg";
import confidentialityImpactHigh from "resources/confidentialityHigh.svg";
import confidentialityImpactLow from "resources/confidentialityLow.svg";
import confidentialityImpactNone from "resources/confidentialityNone.svg";
import exploitabilityFunctional from "resources/exploitabilityFunctional.svg";
import exploitabilityHigh from "resources/exploitabilityHigh.svg";
import exploitabilityProof from "resources/exploitabilityProof.svg";
import exploitabilityUnproven from "resources/exploitabilityUnproven.svg";
import integrityImpactHigh from "resources/integrityHigh.svg";
import integrityImpactLow from "resources/integrityLow.svg";
import integrityImpactNone from "resources/integrityNone.svg";
import privilegesRequiredHigh from "resources/privilegesRequiredHigh.svg";
import privilegesRequiredLow from "resources/privilegesRequiredLow.svg";
import privilegesRequiredNone from "resources/privilegesRequiredNone.svg";
import remediationLevelOfficial from "resources/remediationLevelOfficial.svg";
import remediationLevelTemporary from "resources/remediationLevelTemporary.svg";
import remediationLevelUnavailable from "resources/remediationLevelUnavailable.svg";
import remediationLevelWorkaround from "resources/remediationLevelWorkaround.svg";
import reportConfidenceConfirmed from "resources/reportConfidenceConfirmed.svg";
import reportConfidenceReasonable from "resources/reportConfidenceReasonable.svg";
import reportConfidenceUnknown from "resources/reportConfidenceUnknown.svg";
import severityScopeChanged from "resources/severityScopeChanged.svg";
import severityScopeUnchanged from "resources/severityScopeUnchanged.svg";
import userInteractionNone from "resources/userInteractionNone.svg";
import userInteractionRequired from "resources/userInteractionRequired.svg";

interface ISeverityTile {
  color: string;
  name: string;
  value: string;
  valueText: string;
}

const severityImages: Record<string, string> = {
  attackComplexityHigh,
  attackComplexityLow,
  attackVectorAdjacent,
  attackVectorLocal,
  attackVectorNetwork,
  attackVectorPhysical,
  availabilityImpactHigh,
  availabilityImpactLow,
  availabilityImpactNone,
  confidentialityImpactHigh,
  confidentialityImpactLow,
  confidentialityImpactNone,
  exploitabilityFunctional,
  exploitabilityHigh,
  exploitabilityProof,
  exploitabilityUnproven,
  integrityImpactHigh,
  integrityImpactLow,
  integrityImpactNone,
  privilegesRequiredHigh,
  privilegesRequiredLow,
  privilegesRequiredNone,
  remediationLevelOfficial,
  remediationLevelTemporary,
  remediationLevelUnavailable,
  remediationLevelWorkaround,
  reportConfidenceConfirmed,
  reportConfidenceReasonable,
  reportConfidenceUnknown,
  severityScopeChanged,
  severityScopeUnchanged,
  userInteractionNone,
  userInteractionRequired,
};

const SeverityTile: React.FC<ISeverityTile> = ({
  color,
  name,
  value,
  valueText,
}: ISeverityTile): JSX.Element => {
  const { t } = useTranslation();
  const imageName: string = (
    _.first(`${name}${valueText}`.split(" ")) as string
  ).replace(/\W/u, "");

  return (
    <React.StrictMode>
      <div className={"dt center w-90"}>
        <div className={"dtc v-mid w-30 pr2"}>
          <div className={"mw3"}>
            <ReactSVG src={severityImages[imageName]} />
          </div>
        </div>
        <div className={"dtc v-mid w-70"}>
          <span className={"f5"}>
            <b>{t(`searchFindings.tabSeverity.${name}.label`)}</b>
          </span>
          <div>
            <span className={`dib br-100 pa1 ${color}`} />
            <small>&nbsp;{_.capitalize(valueText)}</small>
          </div>
          <small>{value}</small>
          <br />
        </div>
      </div>
    </React.StrictMode>
  );
};

export { ISeverityTile, SeverityTile, severityImages };
