import {
  faCalendar,
  faClock,
  faSkullCrossbones,
  faTriangleExclamation,
  faUnlockKeyhole,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

import { Indicators } from "components/Indicators";
import {
  Indicator,
  IndicatorIcon,
  IndicatorTitle,
  IndicatorValue,
} from "components/Indicators/Indicator";
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
  const { text: severityText } = severityConfigs[severityLevel];
  const { text: statusText, tooltip: statusTooltip } = statusConfigs[status];

  return (
    <Indicators>
      <Indicator>
        <TooltipWrapper
          id={"severityTooltip"}
          message={
            translate.t("searchFindings.header.severity.tooltip") +
            severityLevelTooltip
          }
        >
          <IndicatorIcon>
            <FontAwesomeIcon icon={faTriangleExclamation} />
          </IndicatorIcon>
          <IndicatorTitle>
            {translate.t("searchFindings.header.severity.label")}
          </IndicatorTitle>
          <IndicatorValue>{`${severity} - ${severityText}`}</IndicatorValue>
        </TooltipWrapper>
      </Indicator>
      <Indicator>
        <TooltipWrapper
          id={"statusTooltip"}
          message={
            translate.t("searchFindings.header.status.tooltip") + statusTooltip
          }
        >
          <IndicatorIcon>
            <FontAwesomeIcon icon={faSkullCrossbones} />
          </IndicatorIcon>
          <IndicatorTitle>
            {translate.t("searchFindings.header.status.label")}
          </IndicatorTitle>
          <IndicatorValue>{statusText}</IndicatorValue>
        </TooltipWrapper>
      </Indicator>
      <Indicator>
        <TooltipWrapper
          id={"openVulnsTooltip"}
          message={translate.t("searchFindings.header.openVulns.tooltip")}
        >
          <IndicatorIcon>
            <FontAwesomeIcon icon={faUnlockKeyhole} />
          </IndicatorIcon>
          <IndicatorTitle>
            {translate.t("searchFindings.header.openVulns.label")}
          </IndicatorTitle>
          <IndicatorValue>{openVulns}</IndicatorValue>
        </TooltipWrapper>
      </Indicator>
      <Indicator>
        <TooltipWrapper
          id={"discoveryDateTooltip"}
          message={translate.t("searchFindings.header.discoveryDate.tooltip")}
        >
          <IndicatorIcon>
            <FontAwesomeIcon icon={faCalendar} />
          </IndicatorIcon>
          <IndicatorTitle>
            {translate.t("searchFindings.header.discoveryDate.label")}
          </IndicatorTitle>
          <IndicatorValue>{discoveryDate}</IndicatorValue>
        </TooltipWrapper>
      </Indicator>
      <Indicator>
        <TooltipWrapper
          id={"estRemediationTime"}
          message={translate.t(
            "searchFindings.header.estRemediationTime.tooltip"
          )}
        >
          <IndicatorIcon>
            <FontAwesomeIcon icon={faClock} />
          </IndicatorIcon>
          <IndicatorTitle>
            {translate.t("searchFindings.header.estRemediationTime.label")}
          </IndicatorTitle>
          <IndicatorValue>{estRemediationTime}</IndicatorValue>
        </TooltipWrapper>
      </Indicator>
    </Indicators>
  );
};

export { FindingHeader };
