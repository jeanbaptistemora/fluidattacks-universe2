/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import type { PropsWithChildren } from "react";
import React from "react";

import type { ITextProps } from ".";
import { Text } from ".";

const config: Meta = {
  component: Text,
  title: "components/Text",
};

const Template: Story<PropsWithChildren<ITextProps>> = (props): JSX.Element => (
  <Text {...props} />
);

const Default = Template.bind({});
Default.args = {
  bright: 5,
  children: "Example Text",
  hoverBright: 3,
  hoverTone: "red",
  ml: 5,
  size: 3,
  tone: "dark",
};

export { Default };
export default config;
