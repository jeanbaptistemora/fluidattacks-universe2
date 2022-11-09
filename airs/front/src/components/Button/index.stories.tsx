/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import type { PropsWithChildren } from "react";
import React from "react";
import { FaArrowRight } from "react-icons/fa";

import type { IButtonProps } from ".";
import { Button } from ".";
import { Container } from "../Container";

const config: Meta = {
  component: Button,
  title: "components/Button",
};

const Template: Story<PropsWithChildren<IButtonProps>> = (
  props
): JSX.Element => (
  <Container display={"flex"} justify={"center"} wrap={"wrap"}>
    <Container
      display={"flex"}
      justify={"center"}
      ph={3}
      pv={3}
      width={"50%"}
      widthSm={"100%"}
    >
      <Button {...props} />
    </Container>
    <Container
      bgColor={"#2e2e38"}
      display={"flex"}
      justify={"center"}
      ph={3}
      pv={3}
      width={"50%"}
      widthSm={"100%"}
    >
      <Button {...props} />
    </Container>
  </Container>
);

const Default = Template.bind({});
Default.args = {
  children: "Test",
  variant: "primary",
};

const IconButton: Story = (): JSX.Element => (
  <Button icon={<FaArrowRight />} iconSide={"right"} variant={"tertiary"}>
    {"Go to"}
  </Button>
);

export { Default, IconButton };
export default config;
