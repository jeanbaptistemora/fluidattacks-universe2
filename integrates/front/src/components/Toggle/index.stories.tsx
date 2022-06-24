/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { IToggleProps } from ".";
import { Toggle } from ".";

const config: Meta = {
  component: Toggle,
  title: "components/Toggle",
};

const Template: Story<IToggleProps> = (props): JSX.Element => (
  <Toggle {...props} />
);

const Default = Template.bind({});
Default.args = {
  size: 30,
};

export { Default };
export default config;
