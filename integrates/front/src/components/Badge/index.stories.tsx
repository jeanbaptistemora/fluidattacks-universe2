/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { IBadgeProps } from ".";
import { Badge } from ".";

const config: Meta = {
  component: Badge,
  title: "Components/Badge",
};

const Template: Story<React.PropsWithChildren<IBadgeProps>> = (
  props: React.PropsWithChildren<IBadgeProps>
): JSX.Element => <Badge {...props} />;

const Default = Template.bind({});
Default.args = {
  children: "Test",
  variant: "green",
};

export { Default };
export default config;
