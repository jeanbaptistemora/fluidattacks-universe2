import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import type { FC } from "react";

import type { IHelpOptionProps } from "./types";

import { Button } from "components/Button";
import { Col, Row } from "components/Layout";
import { Text } from "components/Text";

const HelpOption: FC<IHelpOptionProps> = ({
  description,
  icon,
  onClick,
  title,
}): JSX.Element => {
  return (
    <Button onClick={onClick}>
      <Row>
        <Col lg={10}>
          <Text size={"xs"}>
            <FontAwesomeIcon icon={icon} />
          </Text>
        </Col>
        <Col lg={90}>
          <Row>
            <Col>
              <Text>{title}</Text>
            </Col>
          </Row>
          <Row>
            <Col>
              <Text bright={9} mt={1} size={"xs"} tone={"light"}>
                {description}
              </Text>
            </Col>
          </Row>
        </Col>
      </Row>
    </Button>
  );
};

export { HelpOption };
