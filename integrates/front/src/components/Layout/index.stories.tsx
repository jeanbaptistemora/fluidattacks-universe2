/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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
      <p>{"start (default)"}</p>
      <Row>
        <Col lg={50} md={50} sm={50}>
          <LargeBox />
        </Col>
        <Col lg={50} md={50} sm={50}>
          <Box />
        </Col>
      </Row>
      <p>{"center"}</p>
      <Row align={"center"}>
        <Col lg={50} md={50} sm={50}>
          <LargeBox />
        </Col>
        <Col lg={50} md={50} sm={50}>
          <Box />
        </Col>
      </Row>
      <p>{"end"}</p>
      <Row align={"end"}>
        <Col lg={50} md={50} sm={50}>
          <LargeBox />
        </Col>
        <Col lg={50} md={50} sm={50}>
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
      <p>{"around"}</p>
      <Row justify={"around"}>
        <Col lg={20} md={20} sm={20}>
          <Box />
        </Col>
        <Col lg={20} md={20} sm={20}>
          <Box />
        </Col>
        <Col lg={20} md={20} sm={20}>
          <Box />
        </Col>
      </Row>
      <p>{"between"}</p>
      <Row justify={"between"}>
        <Col lg={20} md={20} sm={20}>
          <Box />
        </Col>
        <Col lg={20} md={20} sm={20}>
          <Box />
        </Col>
        <Col lg={20} md={20} sm={20}>
          <Box />
        </Col>
      </Row>
      <p>{"evenly"}</p>
      <Row justify={"evenly"}>
        <Col lg={20} md={20} sm={20}>
          <Box />
        </Col>
        <Col lg={20} md={20} sm={20}>
          <Box />
        </Col>
        <Col lg={20} md={20} sm={20}>
          <Box />
        </Col>
      </Row>
    </React.Fragment>
  );
};

const Justification: Story = (): JSX.Element => {
  return (
    <React.Fragment>
      <p>{"start (default)"}</p>
      <Row>
        <Col lg={50} md={50} sm={50}>
          <Box />
        </Col>
      </Row>
      <p>{"center"}</p>
      <Row justify={"center"}>
        <Col lg={50} md={50} sm={50}>
          <Box />
        </Col>
      </Row>
      <p>{"end"}</p>
      <Row justify={"end"}>
        <Col lg={50} md={50} sm={50}>
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
        <Col lg={10} md={20} sm={25}>
          <Box />
        </Col>
        <Col lg={80} md={60} sm={50}>
          <Box />
        </Col>
        <Col lg={10} md={20} sm={25}>
          <Box />
        </Col>
      </Row>
      <Row>
        <Col lg={10} md={20} sm={25}>
          <Box />
        </Col>
        <Col lg={90} md={80} sm={75}>
          <Box />
        </Col>
      </Row>
      <Row>
        <Col lg={80} md={70} sm={50}>
          <Box />
        </Col>
        <Col lg={20} md={30} sm={50}>
          <Box />
        </Col>
      </Row>
    </React.Fragment>
  );
};

export { Alignment, AutoWidth, Distribution, Justification, Responsive };
export default config;
