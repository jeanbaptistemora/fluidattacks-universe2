/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { ICtaBannerProps } from "./types";

import { CtaBanner } from ".";

const config: Meta = {
  component: CtaBanner,
  title: "components/CtaBanner",
};

const Template: Story<React.PropsWithChildren<ICtaBannerProps>> = (
  props
): JSX.Element => <CtaBanner {...props} />;

const Default = Template.bind({});
Default.args = {
  image: "airs/solutions/Index/application-security-solutions",
  paragraph:
    "This is a test paragraph that should show the behavior of the CTA",
  title: "This is a test title",
};

export { Default };
export default config;
