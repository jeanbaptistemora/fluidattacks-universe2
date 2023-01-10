import {
  faCalendarDay,
  faClock,
  faHeartPulse,
  faSquareCaretDown,
  faUnlock,
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

  const remediatedLabel =
    statusText === t("searchFindings.header.status.stateLabel.closed")
      ? t("searchFindings.header.riskExposure.remediated")
      : t("searchFindings.header.riskExposure.unremediated");

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
                  {remediatedLabel}
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
                      {t("searchFindings.header.riskExposure.label")}
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
                  <Text>{t("searchFindings.header.status.label")}</Text>
                </Gap>
              </Row>
            </Card>
          </Col>
          <Col lg={20} md={50} sm={100}>
            <Card float={true} title={`${openVulns}`}>
              <Gap>
                <FontAwesomeIcon
                  color={"#2e2e38"}
                  icon={faUnlock}
                  size={"lg"}
                />
                <Text>{t("searchFindings.header.openVulns.label")}</Text>
              </Gap>
            </Card>
          </Col>
          <Col lg={20} md={50} sm={100}>
            <Card float={true} title={discoveryDate}>
              <Gap>
                <FontAwesomeIcon
                  color={"#2e2e38"}
                  icon={faCalendarDay}
                  size={"lg"}
                />
                <Text>{t("searchFindings.header.discoveryDate.label")}</Text>
              </Gap>
            </Card>
          </Col>
          <Col lg={20} md={50} sm={100}>
            <Card float={true} title={estRemediationTime}>
              <Gap>
                <FontAwesomeIcon color={"#2e2e38"} icon={faClock} size={"lg"} />
                <Text>
                  {t("searchFindings.header.estRemediationTime.label")}
                </Text>
              </Gap>
            </Card>
          </Col>
        </Row>
      </Row>
    </React.StrictMode>
  );
};

export { FindingOverview };
