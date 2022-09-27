/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";
import type { PropsWithChildren } from "react";

import type { IProgressBarProps } from ".";
import { ProgressBar } from ".";

const config: Meta = {
  component: ProgressBar,
  title: "components/ProgressBar",
};

const Template: Story<PropsWithChildren<IProgressBarProps>> = (
  props
): JSX.Element => <ProgressBar {...props} />;

const Default = Template.bind({});
Default.args = {
  percentage: 66,
  progressColor: "blue",
};

export { Default };
export default config;
