/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { IContainerProps } from "./types";

import { Container } from ".";

const config: Meta = {
  component: Container,
  title: "components/Container",
};

const Template: Story<React.PropsWithChildren<IContainerProps>> = (
  props
): JSX.Element => <Container {...props} />;

const Default = Template.bind({});
Default.args = {
  bgColor: "#2e2e38",
  center: true,
  height: "500px",
  width: "500px",
};

const Grid: Story = (): JSX.Element => (
  <Container
    direction={"row"}
    display={"flex"}
    justify={"center"}
    wrap={"wrap"}
  >
    {[...Array(15).keys()].map(
      (el): JSX.Element => (
        <Container
          key={el}
          mv={3}
          ph={3}
          width={"25%"}
          widthMd={"50%"}
          widthSm={"100%"}
        >{`Content ${el}`}</Container>
      )
    )}
  </Container>
);

export { Default, Grid };
export default config;
