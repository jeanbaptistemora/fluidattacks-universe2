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
import { Title } from ".";

const config: Meta = {
  component: Title,
  title: "components/Texts/Title",
};

const Template: Story<PropsWithChildren<ITextProps>> = (props): JSX.Element => (
  <Title {...props} />
);

const Default = Template.bind({});
Default.args = {
  children: "Title",
  fColor: "#2e2e38",
  fSize: "48",
};

export { Default };
export default config;
