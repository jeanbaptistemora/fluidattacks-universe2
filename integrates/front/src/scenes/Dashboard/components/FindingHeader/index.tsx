import React from "react";
import { CircularProgressbar } from "react-circular-progressbar";
import type { CircularProgressbarDefaultProps } from "react-circular-progressbar/dist/types";

import calendarIcon from "resources/calendar.svg";
import defaultIcon from "resources/default_finding_state.svg";
import failIcon from "resources/fail.svg";
import okIcon from "resources/ok.svg";
import vulnerabilitiesIcon from "resources/vulnerabilities.svg";
import style from "scenes/Dashboard/components/FindingHeader/index.css";
import {
  Col100,
  FindingHeaderDetail,
  FindingHeaderGrid,
  FindingHeaderIndicator,
  FindingHeaderLabel,
  Row,
} from "styles/styledComponents";
import { translate } from "utils/translations/translate";

interface IFindingHeaderProps {
  discoveryDate: string;
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
  const { discoveryDate, openVulns, severity, status } = props;
  const SEVERITY_THRESHOLD_CRITICAL: number = 9;
  const SEVERITY_THRESHOLD_HIGH: number = 6.9;
  const SEVERITY_THRESHOLD_MED: number = 3.9;
  const SEVERITY_THRESHOLD_LOW: number = 0.1;
  const severityLevel: "CRITICAL" | "HIGH" | "LOW" | "MED" | "NONE" =
    severity >= SEVERITY_THRESHOLD_CRITICAL
      ? "CRITICAL"
      : severity > SEVERITY_THRESHOLD_HIGH
      ? "HIGH"
      : severity > SEVERITY_THRESHOLD_MED
      ? "MED"
      : severity >= SEVERITY_THRESHOLD_LOW
      ? "LOW"
      : "NONE";
  const { color: severityColor, text: severityText } = severityConfigs[
    severityLevel
  ];
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
    <React.StrictMode>
      <Row>
        <Col100>
          <FindingHeaderGrid>
            <div>
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
              </FindingHeaderDetail>
              <FindingHeaderDetail>
                <FindingHeaderLabel>
                  {translate.t("searchFindings.severityLabel")}
                </FindingHeaderLabel>
                <FindingHeaderIndicator>
                  <b>{severityText}</b>
                </FindingHeaderIndicator>
              </FindingHeaderDetail>
            </div>
            <div>
              <FindingHeaderDetail>
                <img alt={""} height={45} src={statusIcon} width={45} />
              </FindingHeaderDetail>
              <FindingHeaderDetail>
                <FindingHeaderLabel>
                  {translate.t("searchFindings.statusLabel")}
                </FindingHeaderLabel>
                <FindingHeaderIndicator>
                  <b>{statusText}</b>
                </FindingHeaderIndicator>
              </FindingHeaderDetail>
            </div>
            <div>
              <FindingHeaderDetail>
                <img
                  alt={""}
                  height={45}
                  src={vulnerabilitiesIcon}
                  width={45}
                />
              </FindingHeaderDetail>
              <FindingHeaderDetail>
                <FindingHeaderLabel>
                  {translate.t("searchFindings.openVulnsLabel")}
                </FindingHeaderLabel>
                <FindingHeaderIndicator>{openVulns}</FindingHeaderIndicator>
              </FindingHeaderDetail>
            </div>
            <div>
              <FindingHeaderDetail>
                <img alt={""} height={40} src={calendarIcon} width={40} />
              </FindingHeaderDetail>
              <FindingHeaderDetail>
                <FindingHeaderLabel>
                  {translate.t("searchFindings.discoveryDateLabel")}
                </FindingHeaderLabel>
                <FindingHeaderIndicator>{discoveryDate}</FindingHeaderIndicator>
              </FindingHeaderDetail>
            </div>
          </FindingHeaderGrid>
        </Col100>
      </Row>
    </React.StrictMode>
  );
};

export { FindingHeader };
