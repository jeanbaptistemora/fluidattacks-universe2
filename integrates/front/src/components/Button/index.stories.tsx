/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import type { PropsWithChildren } from "react";
import React from "react";

import type { IButtonProps } from ".";
import { Button } from ".";

const config: Meta = {
  component: Button,
  title: "components/Button",
};

const Template: Story<PropsWithChildren<IButtonProps>> = (
  props
): JSX.Element => <Button {...props} />;

const Default = Template.bind({});
Default.args = {
  children: "Test",
  disabled: false,
  variant: "primary",
};

export { Default };
export default config;
