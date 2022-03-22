/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { ExternalLinkProps } from ".";
import { ExternalLink } from ".";

const config: Meta = {
  component: ExternalLink,
  title: "components/ExternalLink",
};

const Template: Story<ExternalLinkProps> = (props): JSX.Element => (
  <ExternalLink {...props} />
);

const Default = Template.bind({});
Default.args = {
  children: "https://fluidattacks.com/",
  href: "https://fluidattacks.com/",
};

export { Default };
export default config;
