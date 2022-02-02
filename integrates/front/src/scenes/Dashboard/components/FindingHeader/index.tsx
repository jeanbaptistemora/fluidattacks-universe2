import React from "react";
import { CircularProgressbar } from "react-circular-progressbar";
import type { CircularProgressbarDefaultProps } from "react-circular-progressbar/dist/types";

import {
  FindingHeaderContainer,
  FindingHeaderDetail,
  FindingHeaderIndicator,
  FindingHeaderLabel,
} from "./styles";

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

const statusConfigs: Record<string, { icon: string; text: string }> = {
  closed: { icon: okIcon, text: translate.t("searchFindings.status.closed") },
  default: { icon: defaultIcon, text: "" },
  open: { icon: failIcon, text: translate.t("searchFindings.status.open") },
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
  function setSeverityLevel(): "CRITICAL" | "HIGH" | "LOW" | "MED" | "NONE" {
    if (severity >= SEVERITY_THRESHOLD_CRITICAL) {
      return "CRITICAL";
    }
    if (severity > SEVERITY_THRESHOLD_HIGH) {
      return "HIGH";
    }
    if (severity > SEVERITY_THRESHOLD_MED) {
      return "MED";
    }
    if (severity >= SEVERITY_THRESHOLD_LOW) {
      return "LOW";
    }

    return "NONE";
  }
  const severityLevel: "CRITICAL" | "HIGH" | "LOW" | "MED" | "NONE" =
    setSeverityLevel();
  const { color: severityColor, text: severityText } =
    severityConfigs[severityLevel];
  const { icon: statusIcon, text: statusText } = statusConfigs[status];
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
          {translate.t("searchFindings.severityLabel")}
          <FindingHeaderIndicator>
            <b>{severityText}</b>
          </FindingHeaderIndicator>
        </FindingHeaderLabel>
      </FindingHeaderDetail>
      <FindingHeaderDetail>
        <img alt={""} height={45} src={statusIcon} width={45} />
        <FindingHeaderLabel>
          {translate.t("searchFindings.statusLabel")}
          <FindingHeaderIndicator>
            <b>{statusText}</b>
          </FindingHeaderIndicator>
        </FindingHeaderLabel>
      </FindingHeaderDetail>
      <FindingHeaderDetail>
        <img alt={""} height={45} src={vulnerabilitiesIcon} width={45} />
        <FindingHeaderLabel>
          {translate.t("searchFindings.openVulnsLabel")}
          <FindingHeaderIndicator>{openVulns}</FindingHeaderIndicator>
        </FindingHeaderLabel>
      </FindingHeaderDetail>
      <FindingHeaderDetail>
        <img alt={""} height={40} src={calendarIcon} width={40} />
        <FindingHeaderLabel>
          {translate.t("searchFindings.discoveryDateLabel")}
          <FindingHeaderIndicator>{discoveryDate}</FindingHeaderIndicator>
        </FindingHeaderLabel>
      </FindingHeaderDetail>
      <FindingHeaderDetail>
        <img alt={""} height={40} src={clockIcon} width={40} />
        <FindingHeaderLabel>
          {translate.t("searchFindings.estRemediationTimeLabel")}
          <FindingHeaderIndicator>{estRemediationTime}</FindingHeaderIndicator>
        </FindingHeaderLabel>
      </FindingHeaderDetail>
    </FindingHeaderContainer>
  );
};

export { FindingHeader };
