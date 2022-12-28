import { faCalendar } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FC } from "react";
import React from "react";
import { useTranslation } from "react-i18next";

import { Card } from "components/Card";
import { InfoDropdown } from "components/InfoDropdown";
import { Col } from "components/Layout/Col";
import { Row } from "components/Layout/Row";
import { Text } from "components/Text";

interface IDaysCardProps {
  days: number;
  info: string;
  title: string;
}

const DaysCard: FC<IDaysCardProps> = (props: IDaysCardProps): JSX.Element => {
  const { info, days, title } = props;
  const { t } = useTranslation();

  return (
    <Card>
      <Row>
        <Text size={"small"} ta={"center"}>
          {title} <InfoDropdown>{info}</InfoDropdown>
        </Text>
      </Row>
      <Row>
        <Row justify={"center"}>
          <Col lg={100} md={100} sm={100}>
            <Text fw={9} size={"big"} ta={"center"}>
              {Math.ceil(days)}{" "}
              {t("organization.tabs.compliance.tabs.overview.cards.days")}{" "}
              <FontAwesomeIcon icon={faCalendar} />
            </Text>
          </Col>
        </Row>
      </Row>
    </Card>
  );
};
export { DaysCard };
