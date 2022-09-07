/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { IBadgeProps } from ".";
import { Badge } from ".";

const config: Meta = {
  component: Badge,
  title: "components/Badge",
};

const Template: Story<React.PropsWithChildren<IBadgeProps>> = (
  props
): JSX.Element => <Badge {...props} />;

const Default = Template.bind({});
Default.args = {
  children: "Test",
  variant: "green",
};

export { Default };
export default config;
