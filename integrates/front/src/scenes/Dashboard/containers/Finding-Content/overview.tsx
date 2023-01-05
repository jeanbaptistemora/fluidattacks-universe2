import { faSquareCaretDown } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import { CVSSFContainer } from "./styles";

import { Card } from "components/Card";
import { Col } from "components/Layout/Col";
import { Gap } from "components/Layout/Gap";
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

const FindingOverview: React.FC<IFindingOverviewProps> = ({
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
  //
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
            <CVSSFContainer variant={"red"}>
              <Card>
                <Text
                  bright={0}
                  fw={9}
                  size={"small"}
                  ta={"start"}
                  tone={"red"}
                >
                  {"Remediate this vulnerability"}
                </Text>
                <br />
                {/* eslint-disable-next-line react/forbid-component-props */}
                <Gap style={{ border: "transparent" }}>
                  <FontAwesomeIcon
                    color={"#bf0b1a"}
                    icon={faSquareCaretDown}
                    size={"2x"}
                  />
                  <Text disp={"inline"} fw={9} size={"big"} ta={"start"}>
                    {"20% "}
                    <Text disp={"inline"} size={"small"} ta={"start"}>
                      {"Total Risk Exposure (CVSSF)"}
                    </Text>
                  </Text>
                </Gap>
              </Card>
            </CVSSFContainer>
          </Col>
          <Col lg={20} md={50} sm={100}>
            <Card>
              <Row>
                <Col>
                  <Text disp={"inline"} fw={9} size={"big"} ta={"start"}>
                    {_.capitalize(status)}
                  </Text>
                </Col>
                <Col>
                  <Tag variant={color}>{severity}</Tag>
                </Col>
              </Row>
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

export { FindingOverview };
