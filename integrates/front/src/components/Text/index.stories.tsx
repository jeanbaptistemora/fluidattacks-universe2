/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import type { PropsWithChildren } from "react";
import React from "react";

import type { ITextProps } from ".";
import { Text } from ".";

const config: Meta = {
  component: Text,
  title: "components/Text",
};

const Template: Story<PropsWithChildren<ITextProps>> = (props): JSX.Element => (
  <Text {...props} />
);

const Default = Template.bind({});
Default.args = {
  bright: 5,
  children: "Example Text",
  mh: 5,
  mv: 0,
  size: 5,
  tone: "dark",
};

export { Default };
export default config;
