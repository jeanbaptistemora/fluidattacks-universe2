/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import { Logo } from ".";

const config: Meta = {
  component: Logo,
  title: "components/Logo",
};

const Template: Story = (props): JSX.Element => <Logo {...props} />;

const Default = Template.bind({});
Default.args = {
  height: 50,
  width: 50,
};

export { Default };
export default config;
