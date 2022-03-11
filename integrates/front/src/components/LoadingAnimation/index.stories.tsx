/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import { LoadingAnimation } from ".";

const config: Meta = {
  component: LoadingAnimation,
  title: "components/LoadingAnimation",
};

const Template: Story = (props): JSX.Element => <LoadingAnimation {...props} />;

const Default = Template.bind({});
Default.args = {
  height: 50,
  width: 50,
};

export { Default };
export default config;
