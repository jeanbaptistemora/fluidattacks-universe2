/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { ICloseTagProps } from ".";
import { CloseTag } from ".";

const config: Meta = {
  component: CloseTag,
  title: "components/CloseTag",
};

const Template: Story<React.PropsWithChildren<ICloseTagProps>> = (
  props
): JSX.Element => <CloseTag {...props} />;

const Default = Template.bind({});
Default.args = {
  onClose: (): void => undefined,
  text: "example text",
};

export { Default };
export default config;
