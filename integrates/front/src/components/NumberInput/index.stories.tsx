/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import type { PropsWithChildren } from "react";
import React from "react";

import type { INumberInputProps } from ".";
import { NumberInput } from ".";

const config: Meta = {
  component: NumberInput,
  title: "components/NumberInput",
};

const Template: Story<PropsWithChildren<INumberInputProps>> = (
  props
): JSX.Element => <NumberInput {...props} />;

const Default = Template.bind({});
Default.args = {
  defaultValue: 1,
  max: 7,
  min: 0,
  tooltipMessage: "Enter to save",
};

export { Default };
export default config;
