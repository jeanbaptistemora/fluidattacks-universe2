/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { IProgressIndicatorProps } from ".";
import { ProgressIndicator } from ".";

const config: Meta = {
  component: ProgressIndicator,
  title: "components/ProgressIndicator",
};

const Template: Story<IProgressIndicatorProps> = (props): JSX.Element => (
  <ProgressIndicator {...props} />
);

const Default = Template.bind({});
Default.args = {
  max: 5,
  value: 2,
};

export { Default };
export default config;
