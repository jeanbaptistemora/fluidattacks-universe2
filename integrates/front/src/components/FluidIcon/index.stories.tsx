/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { IFluidIconProps } from ".";
import { FluidIcon } from ".";

const config: Meta = {
  component: FluidIcon,
  title: "Components/FluidIcon",
};

const Template: Story<IFluidIconProps> = (props): JSX.Element => (
  <FluidIcon {...props} />
);

const Default = Template.bind({});
Default.args = {
  height: "50px",
  icon: "authors",
  width: "50px",
};

export { Default };
export default config;
