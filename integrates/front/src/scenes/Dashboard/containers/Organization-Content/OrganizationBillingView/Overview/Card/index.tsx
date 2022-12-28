import type { FC } from "react";
import React from "react";

import { Card } from "components/Card";
import { InfoDropdown } from "components/InfoDropdown";
import { Col } from "components/Layout/Col";
import { Row } from "components/Layout/Row";
import { Text } from "components/Text";

interface ICardProps {
  content: string;
  info: string;
  title: string;
}

const OverviewCard: FC<ICardProps> = (props: ICardProps): JSX.Element => {
  const { info, content, title } = props;

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
              {content}
            </Text>
          </Col>
        </Row>
      </Row>
    </Card>
  );
};
export { OverviewCard };
