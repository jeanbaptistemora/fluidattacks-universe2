/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import type { PropsWithChildren } from "react";
import React from "react";

import type { IInputProps } from ".";
import { Input } from ".";
import { alphaNumeric } from "utils/validations";

const config: Meta = {
  component: Input,
  title: "components/Input",
};

const Template: Story<PropsWithChildren<IInputProps>> = (
  props
): JSX.Element => <Input {...props} />;

const Default = Template.bind({});
Default.args = {
  placeholder: "Example placeholder",
  type: "text",
  validate: alphaNumeric,
  variant: "solid",
};

export { Default };
export default config;
