import React from "react";
import { CircularProgressbar } from "react-circular-progressbar";
import type { CircularProgressbarDefaultProps } from "react-circular-progressbar/dist/types";

import {
  FindingHeaderContainer,
  FindingHeaderDetail,
  FindingHeaderIndicator,
  FindingHeaderLabel,
} from "./styles";

import { TooltipWrapper } from "components/TooltipWrapper";
import calendarIcon from "resources/calendar.svg";
import clockIcon from "resources/clock-light.svg";
import defaultIcon from "resources/default_finding_state.svg";
import failIcon from "resources/fail.svg";
import okIcon from "resources/ok.svg";
import vulnerabilitiesIcon from "resources/vulnerabilities.svg";
import style from "scenes/Dashboard/components/FindingHeader/index.css";
import { translate } from "utils/translations/translate";

interface IFindingHeaderProps {
  discoveryDate: string;
  estRemediationTime: string;
  openVulns: number;
  severity: number;
  status: "closed" | "default" | "open";
}

const severityConfigs: Record<string, { color: string; text: string }> = {
  CRITICAL: {
    color: "#96030D",
    text: translate.t("searchFindings.criticalSeverity"),
  },
  HIGH: {
    color: "#FF1122",
    text: translate.t("searchFindings.highSeverity"),
  },
  LOW: { color: "#FFBF00", text: translate.t("searchFindings.lowSeverity") },
  MED: {
    color: "#FF7722",
    text: translate.t("searchFindings.mediumSeverity"),
  },
  NONE: {
    color: "#FF7722",
    text: translate.t("searchFindings.noneSeverity"),
  },
};

const statusConfigs: Record<
  string,
  { icon: string; text: string; tooltip: string }
> = {
  closed: {
    icon: okIcon,
    text: translate.t("searchFindings.header.status.stateLabel.closed"),
    tooltip: translate.t("searchFindings.header.status.stateTooltip.closed"),
  },
  default: { icon: defaultIcon, text: "", tooltip: "" },
  open: {
    icon: failIcon,
    text: translate.t("searchFindings.header.status.stateLabel.open"),
    tooltip: translate.t("searchFindings.header.status.stateTooltip.open"),
  },
};

const FindingHeader: React.FC<IFindingHeaderProps> = (
  props: IFindingHeaderProps
): JSX.Element => {
  const { discoveryDate, estRemediationTime, openVulns, severity, status } =
    props;
  const SEVERITY_THRESHOLD_CRITICAL: number = 9;
  const SEVERITY_THRESHOLD_HIGH: number = 6.9;
  const SEVERITY_THRESHOLD_MED: number = 3.9;
  const SEVERITY_THRESHOLD_LOW: number = 0.1;
  function setSeverityLevel(): [
    "CRITICAL" | "HIGH" | "LOW" | "MED" | "NONE",
    string
  ] {
    if (severity >= SEVERITY_THRESHOLD_CRITICAL) {
      return [
        "CRITICAL",
        translate.t("searchFindings.header.severity.level.critical"),
      ];
    }
    if (severity > SEVERITY_THRESHOLD_HIGH) {
      return ["HIGH", translate.t("searchFindings.header.severity.level.high")];
    }
    if (severity > SEVERITY_THRESHOLD_MED) {
      return [
        "MED",
        translate.t("searchFindings.header.severity.level.medium"),
      ];
    }
    if (severity >= SEVERITY_THRESHOLD_LOW) {
      return ["LOW", translate.t("searchFindings.header.severity.level.low")];
    }

    return ["NONE", translate.t("searchFindings.header.severity.level.none")];
  }
  const [severityLevel, severityLevelTooltip] = setSeverityLevel();
  const { color: severityColor, text: severityText } =
    severityConfigs[severityLevel];
  const {
    icon: statusIcon,
    text: statusText,
    tooltip: statusTooltip,
  } = statusConfigs[status];
  const severityStyles: CircularProgressbarDefaultProps["classes"] = {
    background: style.severityCircleBg,
    path: style.severityCirclePath,
    root: style.severityCircle,
    text: style.severityCircleText,
    trail: style.severityCircleTrail,
  };
  const CIRCULAR_PROGRESS_BAR_PARAM1: number = 10;
  const CIRCULAR_PROGRESS_BAR_PARAM2: number = 100;

  return (
    <FindingHeaderContainer>
      <TooltipWrapper
        id={"severityTooltip"}
        message={
          translate.t("searchFindings.header.severity.tooltip") +
          severityLevelTooltip
        }
      >
        <FindingHeaderDetail>
          <CircularProgressbar
            classes={severityStyles}
            styles={{
              path: { stroke: severityColor },
              text: { fill: severityColor },
            }}
            text={`${severity}`}
            value={
              (severity / CIRCULAR_PROGRESS_BAR_PARAM1) *
              CIRCULAR_PROGRESS_BAR_PARAM2
            }
          />
          <FindingHeaderLabel>
            {translate.t("searchFindings.header.severity.label")}
            <FindingHeaderIndicator>
              <b>{severityText}</b>
            </FindingHeaderIndicator>
          </FindingHeaderLabel>
        </FindingHeaderDetail>
      </TooltipWrapper>
      <TooltipWrapper
        id={"statusTooltip"}
        message={
          translate.t("searchFindings.header.status.tooltip") + statusTooltip
        }
      >
        <FindingHeaderDetail>
          <img alt={""} height={45} src={statusIcon} width={45} />
          <FindingHeaderLabel>
            {translate.t("searchFindings.header.status.label")}
            <FindingHeaderIndicator>
              <b>{statusText}</b>
            </FindingHeaderIndicator>
          </FindingHeaderLabel>
        </FindingHeaderDetail>
      </TooltipWrapper>
      <TooltipWrapper
        id={"openVulnsTooltip"}
        message={translate.t("searchFindings.header.openVulns.tooltip")}
      >
        <FindingHeaderDetail>
          <img alt={""} height={45} src={vulnerabilitiesIcon} width={45} />
          <FindingHeaderLabel>
            {translate.t("searchFindings.header.openVulns.label")}
            <FindingHeaderIndicator>{openVulns}</FindingHeaderIndicator>
          </FindingHeaderLabel>
        </FindingHeaderDetail>
      </TooltipWrapper>
      <TooltipWrapper
        id={"discoveryDateTooltip"}
        message={translate.t("searchFindings.header.discoveryDate.tooltip")}
      >
        <FindingHeaderDetail>
          <img alt={""} height={40} src={calendarIcon} width={40} />
          <FindingHeaderLabel>
            {translate.t("searchFindings.header.discoveryDate.label")}
            <FindingHeaderIndicator>{discoveryDate}</FindingHeaderIndicator>
          </FindingHeaderLabel>
        </FindingHeaderDetail>
      </TooltipWrapper>
      <TooltipWrapper
        id={"estRemediationTime"}
        message={translate.t(
          "searchFindings.header.estRemediationTime.tooltip"
        )}
      >
        <FindingHeaderDetail>
          <img alt={""} height={40} src={clockIcon} width={40} />
          <FindingHeaderLabel>
            {translate.t("searchFindings.header.estRemediationTime.label")}
            <FindingHeaderIndicator>
              {estRemediationTime}
            </FindingHeaderIndicator>
          </FindingHeaderLabel>
        </FindingHeaderDetail>
      </TooltipWrapper>
    </FindingHeaderContainer>
  );
};

export { FindingHeader };
