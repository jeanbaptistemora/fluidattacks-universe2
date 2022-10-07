/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { ExternalLinkProps } from "./types";

import { ExternalLink, ExternalLinkOutline, ExternalLinkStandalone } from ".";

const config: Meta = {
  subcomponents: { ExternalLink, ExternalLinkOutline, ExternalLinkStandalone },
  title: "components/ExternalLink",
};

const Template: Story<ExternalLinkProps> = (props): JSX.Element => (
  <ExternalLink {...props} />
);

const TemplateStandalone: Story<ExternalLinkProps> = (props): JSX.Element => (
  <ExternalLinkStandalone {...props} />
);

const TemplateOutline: Story<ExternalLinkProps> = (props): JSX.Element => (
  <ExternalLinkOutline {...props} />
);

const Default = Template.bind({});
Default.args = {
  children: "https://fluidattacks.com/",
  href: "https://fluidattacks.com/",
};

const StandaloneLink = TemplateStandalone.bind({});
StandaloneLink.args = {
  children: "https://fluidattacks.com/",
  href: "https://fluidattacks.com/",
};

const OutlineLink = TemplateOutline.bind({});
OutlineLink.args = {
  children: "https://fluidattacks.com/",
  href: "https://fluidattacks.com/",
};

export { Default, StandaloneLink, OutlineLink };
export default config;
