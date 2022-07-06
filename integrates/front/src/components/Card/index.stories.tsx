/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { ICardProps } from ".";
import { Card } from ".";
import { Col, Row } from "components/Layout";
import { Text } from "components/Text";

const config: Meta = {
  component: Card,
  title: "components/Card",
};

const Template: Story<React.PropsWithChildren<ICardProps>> = (
  props
): JSX.Element => (
  <Row>
    {[...Array(5).keys()].map(
      (el): JSX.Element => (
        <Col key={el} large={"50"} medium={"50"} small={"50"}>
          <Card {...props} />
        </Col>
      )
    )}
  </Row>
);

const Default = Template.bind({});
Default.args = {
  children: (
    <Text>{"Lorem ipsum dolor sit amet, consectetur adipiscing elit."}</Text>
  ),
  title: "Card title",
};

const CardImg = Template.bind({});
CardImg.args = {
  children: (
    <Text>{"Lorem ipsum dolor sit amet, consectetur adipiscing elit."}</Text>
  ),
  img: (
    <img
      alt={"Fluid logo"}
      src={
        "https://gitlab.com/uploads/-/system/project/avatar/20741933/logo.png"
      }
    />
  ),
  title: "Card title",
};

export { Default, CardImg };
export default config;
