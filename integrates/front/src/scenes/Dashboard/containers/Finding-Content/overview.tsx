import React from "react";

import { Card } from "components/Card";
import { Col } from "components/Layout/Col";
import { Row } from "components/Layout/Row";
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
  // Const { t } = useTranslation();

  return (
    <React.StrictMode>
      <Row>
        <Row>
          <Col lg={25} md={50} sm={100}>
            <Card title={"Remediate this vulnerability"}>
              <Text>{"placeholder 20% vuln (CVSSF)"}</Text>
            </Card>
          </Col>
          <Col lg={25} md={50} sm={100}>
            <Card title={`${status} ${severity}`}>
              <Text>{"status and severity"}</Text>
            </Card>
          </Col>
          <Col lg={25} md={50} sm={100}>
            <Card title={`${openVulns}`}>
              <Text>{"status and severity"}</Text>
            </Card>
          </Col>
          <Col lg={25} md={50} sm={100}>
            <Card title={discoveryDate}>
              <Text>{"First Reported"}</Text>
            </Card>
          </Col>
          <Col lg={25} md={50} sm={100}>
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
