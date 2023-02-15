/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { IEmptyProps } from "./types";

import { Empty } from ".";
import { searchingFindings } from "resources";

const config: Meta = {
  component: Empty,
  title: "components/Empty",
};

const Template: Story<IEmptyProps> = (props): JSX.Element => (
  <Empty {...props} />
);

const Default = Template.bind({});
Default.args = {
  loading: true,
  srcImage: searchingFindings,
  subtitle: "Test",
  title: "Example of title",
};

export { Default };
export default config;
