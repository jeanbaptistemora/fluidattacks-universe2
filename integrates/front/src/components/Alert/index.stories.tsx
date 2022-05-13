/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { IAlertProps } from ".";
import { Alert } from ".";

const config: Meta = {
  component: Alert,
  title: "components/Alert",
};

const Template: Story<React.PropsWithChildren<IAlertProps>> = (
  props
): JSX.Element => <Alert {...props} />;

const Default = Template.bind({});
Default.args = {
  children: "Test",
  variant: "success",
};

export { Default };
export default config;
