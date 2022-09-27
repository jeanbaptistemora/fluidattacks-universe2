/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";
import type { PropsWithChildren } from "react";

import type { IInfoDropdownProps } from ".";
import { InfoDropdown } from ".";

const config: Meta = {
  component: InfoDropdown,
  title: "components/InfoDropdown",
};

const Template: Story<PropsWithChildren<IInfoDropdownProps>> = (
  props
): JSX.Element => <InfoDropdown {...props}>{"Information"}</InfoDropdown>;

const Default = Template.bind({});
Default.args = {
  alignDropdown: "right",
  size: 2,
};

export { Default };
export default config;
