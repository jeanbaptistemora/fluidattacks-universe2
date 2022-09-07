/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { ILoadingProps } from ".";
import { Loading } from ".";

const config: Meta = {
  component: Loading,
  title: "components/Loading",
};

const Template: Story<ILoadingProps> = (props): JSX.Element => (
  <Loading {...props} />
);

const Default = Template.bind({});
Default.args = {
  size: 30,
};

export { Default };
export default config;
