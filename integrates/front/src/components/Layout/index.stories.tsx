/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";
import styled from "styled-components";

import { Col, Row } from ".";

const config: Meta = {
  component: Row,
  subcomponents: { Col },
  title: "components/Layout",
};

const Box = styled.div.attrs({ className: "bg-gray mb3 pa3" })``;

const AutoWidth: Story = (): JSX.Element => {
  return (
    <React.Fragment>
      <Row>
        <Col>
          <Box />
        </Col>
      </Row>
      <Row>
        <Col>
          <Box />
        </Col>
        <Col>
          <Box />
        </Col>
        <Col>
          <Box />
        </Col>
      </Row>
    </React.Fragment>
  );
};

const Responsive: Story = (): JSX.Element => {
  return (
    <React.Fragment>
      <Row>
        <Col large={"10"} medium={"20"} small={"25"}>
          <Box />
        </Col>
        <Col large={"80"} medium={"60"} small={"50"}>
          <Box />
        </Col>
        <Col large={"10"} medium={"20"} small={"25"}>
          <Box />
        </Col>
      </Row>
      <Row>
        <Col large={"10"} medium={"20"} small={"25"}>
          <Box />
        </Col>
        <Col large={"90"} medium={"80"} small={"75"}>
          <Box />
        </Col>
      </Row>
      <Row>
        <Col large={"80"} medium={"70"} small={"50"}>
          <Box />
        </Col>
        <Col large={"20"} medium={"30"} small={"50"}>
          <Box />
        </Col>
      </Row>
    </React.Fragment>
  );
};

export { AutoWidth, Responsive };
export default config;
