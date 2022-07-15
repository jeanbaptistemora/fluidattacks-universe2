/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { ITooltipProps } from ".";
import { Tooltip } from ".";
import { Text } from "components/Text";

const config: Meta = {
  component: Tooltip,
  title: "components/Tooltip",
};

const Template: Story<ITooltipProps> = (props): JSX.Element => (
  <Tooltip {...props}>
    <Text mb={3} mt={3}>
      {"Hover this text"}
    </Text>
  </Tooltip>
);

const Default = Template.bind({});
Default.args = {
  tip: "Example tip",
};

export { Default };
export default config;
