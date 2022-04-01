import {
  faCalendarTimes,
  faClock,
  faSkullCrossbones,
  faTriangleExclamation,
  faUnlockKeyhole,
} from "@fortawesome/free-solid-svg-icons";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IBadgeProps } from "components/Badge";
import { Badge } from "components/Badge";
import { Indicator, Indicators } from "components/Indicators";
import { TooltipWrapper } from "components/TooltipWrapper";
import defaultIcon from "resources/default_finding_state.svg";
import failIcon from "resources/fail.svg";
import okIcon from "resources/ok.svg";
import { translate } from "utils/translations/translate";

interface IFindingHeaderProps {
  discoveryDate: string;
  estRemediationTime: string;
  openVulns: number;
  severity: number;
  status: "closed" | "default" | "open";
}

const severityConfigs: Record<
  string,
  { color: IBadgeProps["variant"]; text: string }
> = {
  CRITICAL: {
    color: "red",
    text: translate.t("searchFindings.criticalSeverity"),
  },
  HIGH: {
    color: "red",
    text: translate.t("searchFindings.highSeverity"),
  },
  LOW: { color: "gray", text: translate.t("searchFindings.lowSeverity") },
  MED: {
    color: "orange",
    text: translate.t("searchFindings.mediumSeverity"),
  },
  NONE: {
    color: "gray",
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

const FindingHeader: React.FC<IFindingHeaderProps> = ({
  discoveryDate,
  estRemediationTime,
  openVulns,
  severity,
  status,
}: IFindingHeaderProps): JSX.Element => {
  const { t } = useTranslation();
  const SEVERITY_THRESHOLD_CRITICAL: number = 9;
  const SEVERITY_THRESHOLD_HIGH: number = 6.9;
  const SEVERITY_THRESHOLD_MED: number = 3.9;
  const SEVERITY_THRESHOLD_LOW: number = 0.1;
  function setSeverityLevel(): [
    "CRITICAL" | "HIGH" | "LOW" | "MED" | "NONE",
    string
  ] {
    if (severity >= SEVERITY_THRESHOLD_CRITICAL) {
      return ["CRITICAL", t("searchFindings.header.severity.level.critical")];
    }
    if (severity > SEVERITY_THRESHOLD_HIGH) {
      return ["HIGH", t("searchFindings.header.severity.level.high")];
    }
    if (severity > SEVERITY_THRESHOLD_MED) {
      return ["MED", t("searchFindings.header.severity.level.medium")];
    }
    if (severity >= SEVERITY_THRESHOLD_LOW) {
      return ["LOW", t("searchFindings.header.severity.level.low")];
    }

    return ["NONE", t("searchFindings.header.severity.level.none")];
  }
  const [severityLevel, severityLevelTooltip] = setSeverityLevel();
  const { color, text: severityText } = severityConfigs[severityLevel];
  const { text: statusText, tooltip: statusTooltip } = statusConfigs[status];

  return (
    <Indicators>
      <Indicator
        icon={faTriangleExclamation}
        title={t("searchFindings.header.severity.label")}
      >
        <TooltipWrapper
          id={"severityTooltip"}
          message={
            t("searchFindings.header.severity.tooltip") + severityLevelTooltip
          }
        >
          <Badge variant={color}>{severity}</Badge>
          &nbsp;{"-"}&nbsp;
          {severityText}
        </TooltipWrapper>
      </Indicator>
      <Indicator
        icon={faSkullCrossbones}
        title={t("searchFindings.header.status.label")}
      >
        <TooltipWrapper
          id={"statusTooltip"}
          message={t("searchFindings.header.status.tooltip") + statusTooltip}
        >
          {statusText}
        </TooltipWrapper>
      </Indicator>
      <Indicator
        icon={faUnlockKeyhole}
        title={t("searchFindings.header.openVulns.label")}
      >
        <TooltipWrapper
          id={"openVulnsTooltip"}
          message={t("searchFindings.header.openVulns.tooltip")}
        >
          {openVulns}
        </TooltipWrapper>
      </Indicator>
      <Indicator
        icon={faCalendarTimes}
        title={t("searchFindings.header.discoveryDate.label")}
      >
        <TooltipWrapper
          id={"discoveryDateTooltip"}
          message={t("searchFindings.header.discoveryDate.tooltip")}
        >
          {discoveryDate}
        </TooltipWrapper>
      </Indicator>
      <Indicator
        icon={faClock}
        title={t("searchFindings.header.estRemediationTime.label")}
      >
        <TooltipWrapper
          id={"estRemediationTime"}
          message={t("searchFindings.header.estRemediationTime.tooltip")}
        >
          {estRemediationTime}
        </TooltipWrapper>
      </Indicator>
    </Indicators>
  );
};

export { FindingHeader };
