/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { IAnnounceProps } from ".";
import { Announce } from ".";

const config: Meta = {
  component: Announce,
  title: "components/Announce",
};

const Template: Story<IAnnounceProps> = (props): JSX.Element => (
  <Announce {...props} />
);

const Default = Template.bind({});
Default.args = {
  message: "Test message",
};

export { Default };
export default config;
