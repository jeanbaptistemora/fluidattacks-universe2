/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import { CardHeader } from "./Header";

import { Card, CardBody } from ".";
import { Col, Row } from "components/Layout";

const config: Meta = {
  component: Card,
  subcomponents: { CardBody, CardHeader },
  title: "components/Card",
};

const Default: Story = (): JSX.Element => {
  return (
    <Row>
      <Col large={"50"} medium={"50"} small={"50"}>
        <Card>
          <CardHeader>{"Lorem Ipsum"}</CardHeader>
          <CardBody>
            <p>{"Lorem ipsum dolor sit amet, consectetur adipiscing elit."}</p>
          </CardBody>
        </Card>
      </Col>
      <Col large={"50"} medium={"50"} small={"50"}>
        <Card>
          <CardHeader>{"Lorem Ipsum"}</CardHeader>
          <CardBody>
            <p>{"Lorem ipsum dolor sit amet, consectetur adipiscing elit."}</p>
          </CardBody>
        </Card>
      </Col>
    </Row>
  );
};

export { Default };
export default config;
