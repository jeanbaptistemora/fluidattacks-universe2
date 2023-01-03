import React from "react";
import { useTranslation } from "react-i18next";

import { Card } from "components/Card";
import { Col } from "components/Layout/Col";
import { Row } from "components/Layout/Row";
import type { ITagProps } from "components/Tag";
import { Tag } from "components/Tag";
import { Text } from "components/Text";

interface IFindingOverviewProps {
  discoveryDate: string;
  estRemediationTime: string;
  openVulns: number;
  severity: number;
  status: string;
}

const OrganizationGroupOverview: React.FC<IFindingOverviewProps> = ({
  discoveryDate,
  estRemediationTime,
  openVulns,
  severity,
  status,
}: IFindingOverviewProps): JSX.Element => {
  const { t } = useTranslation();

  const severityConfigs: Record<
    string,
    { color: ITagProps["variant"]; text: string }
  > = {
    CRITICAL: {
      color: "red",
      text: t("searchFindings.criticalSeverity"),
    },
    HIGH: {
      color: "red",
      text: t("searchFindings.highSeverity"),
    },
    LOW: { color: "gray", text: t("searchFindings.lowSeverity") },
    MED: {
      color: "orange",
      text: t("searchFindings.mediumSeverity"),
    },
    NONE: {
      color: "gray",
      text: t("searchFindings.noneSeverity"),
    },
  };

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

  const [severityLevel] = setSeverityLevel();
  const { color } = severityConfigs[severityLevel];

  return (
    <React.StrictMode>
      <Row>
        <Row>
          <Col lg={20} md={50} sm={100}>
            <Card title={"Remediate this vulnerability"}>
              <Tag variant={color}>{severity}</Tag>
              <Text>{"placeholder 20% vuln (CVSSF)"}</Text>
            </Card>
          </Col>
          <Col lg={20} md={50} sm={100}>
            <Card title={`${status} ${severity}`}>
              <Text>{"status and severity"}</Text>
            </Card>
          </Col>
          <Col lg={20} md={50} sm={100}>
            <Card title={`${openVulns}`}>
              <Text>{"status and severity"}</Text>
            </Card>
          </Col>
          <Col lg={20} md={50} sm={100}>
            <Card title={discoveryDate}>
              <Text>{"First Reported"}</Text>
            </Card>
          </Col>
          <Col lg={20} md={50} sm={100}>
            <Card title={estRemediationTime}>
              <Text>{"Remediation time"}</Text>
            </Card>
          </Col>
        </Row>
      </Row>
    </React.StrictMode>
  );
};

export { OrganizationGroupOverview };
