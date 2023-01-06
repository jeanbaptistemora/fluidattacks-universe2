import {
  faHeartPulse,
  faSquareCaretDown,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import { CVSSFContainer } from "./styles";

import { Card } from "components/Card";
import { Col } from "components/Layout/Col";
import { Gap } from "components/Layout/Gap";
import { Row } from "components/Layout/Row";
import { Text } from "components/Text";
import { Tooltip } from "components/Tooltip";
import { VulnTag } from "components/VulnTag";
import failIcon from "resources/fail.svg";
import okIcon from "resources/ok.svg";

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

  const statusConfigs: Record<
    string,
    { icon: string; text: string; tooltip: string }
  > = {
    SAFE: {
      icon: okIcon,
      text: t("searchFindings.header.status.stateLabel.closed"),
      tooltip: t("searchFindings.header.status.stateTooltip.closed"),
    },
    VULNERABLE: {
      icon: failIcon,
      text: t("searchFindings.header.status.stateLabel.open"),
      tooltip: t("searchFindings.header.status.stateTooltip.open"),
    },
  };
  const { text: statusText, tooltip: statusTooltip } = statusConfigs[status];

  const cvssfColor =
    statusText === t("searchFindings.header.status.stateLabel.closed")
      ? "green"
      : "red";

  const cvssfTextColor =
    statusText === t("searchFindings.header.status.stateLabel.closed")
      ? "dark"
      : "red";

  return (
    <React.StrictMode>
      <Row>
        <Row>
          <Col lg={20} md={50} sm={100}>
            <CVSSFContainer variant={cvssfColor}>
              <Card float={true}>
                <Text
                  bright={0}
                  fw={9}
                  size={"small"}
                  ta={"start"}
                  tone={cvssfTextColor}
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
            <Card float={true}>
              <Row>
                <Col>
                  <Tooltip
                    id={"statusTooltip"}
                    tip={
                      t("searchFindings.header.status.tooltip") + statusTooltip
                    }
                  >
                    <Text disp={"inline"} fw={9} size={"big"} ta={"start"}>
                      {_.capitalize(status)}
                    </Text>
                  </Tooltip>
                </Col>
                <Col>
                  <Text disp={"inline"} size={"medium"} ta={"end"}>
                    <VulnTag value={severity} />
                  </Text>
                </Col>
              </Row>
              <Row>
                <Gap>
                  <FontAwesomeIcon
                    color={"#2e2e38"}
                    icon={faHeartPulse}
                    size={"lg"}
                  />
                  <Text size={"small"}>{"status and severity"}</Text>
                </Gap>
              </Row>
            </Card>
          </Col>
          <Col lg={20} md={50} sm={100}>
            <Card float={true} title={`${openVulns}`}>
              <Text>{"status and severity"}</Text>
            </Card>
          </Col>
          <Col lg={20} md={50} sm={100}>
            <Card float={true} title={discoveryDate}>
              <Text>{"First Reported"}</Text>
            </Card>
          </Col>
          <Col lg={20} md={50} sm={100}>
            <Card float={true} title={estRemediationTime}>
              <Text>{"Remediation time"}</Text>
            </Card>
          </Col>
        </Row>
      </Row>
    </React.StrictMode>
  );
};

export { FindingOverview };
