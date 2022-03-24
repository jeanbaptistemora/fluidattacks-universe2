/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";
import styled from "styled-components";

import { Col, Row } from ".";

const config: Meta = {
  subcomponents: { Col, Row },
  title: "components/Layout",
};

const Box = styled.div.attrs({ className: "bg-gray pa3" })``;
const LargeBox = styled(Box)`
  height: 8rem;
`;

const Alignment: Story = (): JSX.Element => {
  return (
    <React.Fragment>
      <h1>{"Alignment"}</h1>
      <p>{"flex-start (default)"}</p>
      <Row>
        <Col large={"50"} medium={"50"} small={"50"}>
          <LargeBox />
        </Col>
        <Col large={"50"} medium={"50"} small={"50"}>
          <Box />
        </Col>
      </Row>
      <p>{"center"}</p>
      <Row align={"center"}>
        <Col large={"50"} medium={"50"} small={"50"}>
          <LargeBox />
        </Col>
        <Col large={"50"} medium={"50"} small={"50"}>
          <Box />
        </Col>
      </Row>
      <p>{"flex-end"}</p>
      <Row align={"flex-end"}>
        <Col large={"50"} medium={"50"} small={"50"}>
          <LargeBox />
        </Col>
        <Col large={"50"} medium={"50"} small={"50"}>
          <Box />
        </Col>
      </Row>
    </React.Fragment>
  );
};

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

const Distribution: Story = (): JSX.Element => {
  return (
    <React.Fragment>
      <p>{"space-around"}</p>
      <Row justify={"space-around"}>
        <Col large={"20"} medium={"20"} small={"20"}>
          <Box />
        </Col>
        <Col large={"20"} medium={"20"} small={"20"}>
          <Box />
        </Col>
        <Col large={"20"} medium={"20"} small={"20"}>
          <Box />
        </Col>
      </Row>
      <p>{"space-between"}</p>
      <Row justify={"space-between"}>
        <Col large={"20"} medium={"20"} small={"20"}>
          <Box />
        </Col>
        <Col large={"20"} medium={"20"} small={"20"}>
          <Box />
        </Col>
        <Col large={"20"} medium={"20"} small={"20"}>
          <Box />
        </Col>
      </Row>
      <p>{"space-evenly"}</p>
      <Row justify={"space-evenly"}>
        <Col large={"20"} medium={"20"} small={"20"}>
          <Box />
        </Col>
        <Col large={"20"} medium={"20"} small={"20"}>
          <Box />
        </Col>
        <Col large={"20"} medium={"20"} small={"20"}>
          <Box />
        </Col>
      </Row>
    </React.Fragment>
  );
};

const Justification: Story = (): JSX.Element => {
  return (
    <React.Fragment>
      <p>{"flex-start (default)"}</p>
      <Row>
        <Col large={"50"} medium={"50"} small={"50"}>
          <Box />
        </Col>
      </Row>
      <p>{"center"}</p>
      <Row justify={"center"}>
        <Col large={"50"} medium={"50"} small={"50"}>
          <Box />
        </Col>
      </Row>
      <p>{"flex-end"}</p>
      <Row justify={"flex-end"}>
        <Col large={"50"} medium={"50"} small={"50"}>
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

export { Alignment, AutoWidth, Distribution, Justification, Responsive };
export default config;
