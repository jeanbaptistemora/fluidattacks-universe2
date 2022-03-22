/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import { useArgs } from "@storybook/addons";
import type { Meta, Story } from "@storybook/react";
import React, { useCallback } from "react";

import type { ISwitchProps } from ".";
import { Switch } from ".";

const config: Meta = {
  component: Switch,
  title: "components/Switch",
};

const Template: Story<ISwitchProps> = (props: ISwitchProps): JSX.Element => {
  const [, setArgs] = useArgs();
  const handleChange = useCallback((): void => {
    setArgs({ checked: !props.checked });
  }, [props, setArgs]);

  return <Switch {...props} onChange={handleChange} />;
};

const Default = Template.bind({});
Default.args = {
  checked: true,
  disabled: false,
};

export { Default };
export default config;
