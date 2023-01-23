/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { IPillProps } from ".";
import { Pill } from ".";

const config: Meta = {
  component: Pill,
  title: "components/Pill",
};

const Template: Story<React.PropsWithChildren<IPillProps>> = (
  props
): JSX.Element => <Pill {...props} />;

const Default = Template.bind({});
Default.args = {
  textL: "text1",
  textR: "text2",
  variant: "darkRed",
};

export { Default };
export default config;
