import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import type { ITagProps } from "./styles";
import { NumberDisplay, Tag, VulnDisplay } from "./styles";

import { Tooltip } from "components/Tooltip";

interface IStatus {
  value: number | undefined;
}

const VulnTag: React.FC<IStatus> = ({ value }: IStatus): JSX.Element => {
  const { t } = useTranslation();
  const SEVERITY_THRESHOLD_CRITICAL: number = 9;
  const SEVERITY_THRESHOLD_HIGH: number = 6.9;
  const SEVERITY_THRESHOLD_MED: number = 3.9;
  const SEVERITY_THRESHOLD_LOW: number = 0.1;

  function setSeverityLevel(
    severity?: number
  ): ["CRITICAL" | "HIGH" | "LOW" | "MED" | "NONE", string] {
    if (severity === undefined) {
      return ["NONE", t("searchFindings.header.severity.level.none")];
    }
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

  const severityConfigs: Record<
    string,
    { color: ITagProps["variant"]; text: string }
  > = {
    CRITICAL: {
      color: "deepRed",
      text: t("searchFindings.criticalSeverity"),
    },
    HIGH: {
      color: "red",
      text: t("searchFindings.highSeverity"),
    },
    LOW: { color: "yellow", text: t("searchFindings.lowSeverity") },
    MED: {
      color: "orange",
      text: t("searchFindings.mediumSeverity"),
    },
    NONE: {
      color: "none",
      text: t("searchFindings.noneSeverity"),
    },
  };

  const [severityLevel, severityLevelTooltip] = setSeverityLevel(value);
  const { color, text: severityText } = severityConfigs[severityLevel];
  const formatedStatus: string = _.capitalize(String(value));

  return (
    <Tooltip
      id={"severityTooltip"}
      tip={t("searchFindings.header.severity.tooltip") + severityLevelTooltip}
    >
      <Tag>
        <NumberDisplay variant={color}>
          {formatedStatus.split(" ")[0]}
        </NumberDisplay>
        <VulnDisplay variant={color}>{severityText}</VulnDisplay>
      </Tag>
    </Tooltip>
  );
};

export type { IStatus };
export { VulnTag };
