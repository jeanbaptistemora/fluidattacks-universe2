import { faDownLong, faUpLong } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FC } from "react";
import React from "react";

import { Card } from "components/Card";
import { InfoDropdown } from "components/InfoDropdown";
import { Col } from "components/Layout/Col";
import { Row } from "components/Layout/Row";
import { Text } from "components/Text";

interface ITrendCardProps {
  info: string;
  trend: number;
  title: string;
}

const getArrow: (trend: number) => JSX.Element = (trend: number): JSX.Element =>
  trend < 0 ? (
    <FontAwesomeIcon color={"#BF0B1A"} icon={faDownLong} />
  ) : (
    <FontAwesomeIcon color={"#009245"} icon={faUpLong} />
  );

const TrendCard: FC<ITrendCardProps> = (
  props: ITrendCardProps
): JSX.Element => {
  const { info, trend, title } = props;

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
              {trend} {trend === 0 ? undefined : getArrow(trend)}
            </Text>
          </Col>
        </Row>
      </Row>
    </Card>
  );
};
export { TrendCard };
