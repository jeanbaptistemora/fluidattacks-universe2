import React from "react";
import { ReactSVG } from "react-svg";
import _ from "lodash";
import attackComplexityHigh from "resources/attackComplexityHigh.svg";
import attackComplexityLow from "resources/attackComplexityLow.svg";
import { useTranslation } from "react-i18next";

interface ISeverityTile {
  color: string;
  name: string;
  value: string;
  valueText: string;
}

const severityImages: Record<string, string> = {
  attackComplexityHigh,
  attackComplexityLow,
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
