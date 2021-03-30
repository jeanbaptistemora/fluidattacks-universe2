import React from "react";
import { ReactSVG } from "react-svg";
import _ from "lodash";
import attackComplexityHigh from "resources/attackComplexityHigh.svg";
import attackComplexityLow from "resources/attackComplexityLow.svg";
import attackVectorAdjacent from "resources/attackVectorAdjacent.svg";
import attackVectorLocal from "resources/attackVectorLocal.svg";
import attackVectorNetwork from "resources/attackVectorNetwork.svg";
import attackVectorPhysical from "resources/attackVectorPhysical.svg";
import availabilityImpactHigh from "resources/availabilityImpactHigh.svg";
import availabilityImpactLow from "resources/availabilityImpactLow.svg";
import availabilityImpactNone from "resources/availabilityImpactNone.svg";
import exploitabilityFunctional from "resources/exploitabilityFunctional.svg";
import exploitabilityHigh from "resources/exploitabilityHigh.svg";
import exploitabilityProof from "resources/exploitabilityProof.svg";
import exploitabilityUnproven from "resources/exploitabilityUnproven.svg";
import privilegesRequiredHigh from "resources/privilegesRequiredHigh.svg";
import privilegesRequiredLow from "resources/privilegesRequiredLow.svg";
import privilegesRequiredNone from "resources/privilegesRequiredNone.svg";
import severityScopeChanged from "resources/severityScopeChanged.svg";
import severityScopeUnchanged from "resources/severityScopeUnchanged.svg";
import { useTranslation } from "react-i18next";
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
  exploitabilityFunctional,
  exploitabilityHigh,
  exploitabilityProof,
  exploitabilityUnproven,
  privilegesRequiredHigh,
  privilegesRequiredLow,
  privilegesRequiredNone,
  severityScopeChanged,
  severityScopeUnchanged,
  userInteractionNone,
  userInteractionRequired,
};

export const SeverityTile: React.FC<ISeverityTile> = ({
  color,
  name,
  value,
  valueText,
}: ISeverityTile): JSX.Element => {
  const { t } = useTranslation();
  const imageName: string = (_.first(
    `${name}${valueText}`.split(" ")
  ) as string).replace(/\W/u, "");

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
            <b>{t(`searchFindings.tabSeverity.${name}`)}</b>
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
