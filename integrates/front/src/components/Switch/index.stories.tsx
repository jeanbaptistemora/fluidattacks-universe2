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
  const { checked } = props;
  const handleChange = useCallback((): void => {
    setArgs({ checked: !checked });
  }, [checked, setArgs]);

  return <Switch {...props} onChange={handleChange} />;
};

const Default = Template.bind({});
Default.args = {
  checked: true,
  disabled: false,
};

const WithShortLabel = Template.bind({});
WithShortLabel.args = {
  checked: true,
  label: { off: "No", on: "Yes" },
};

const WithLongLabel = Template.bind({});
WithLongLabel.args = {
  checked: true,
  label: { off: "Inactive", on: "Active" },
};

export { Default, WithLongLabel, WithShortLabel };
export default config;
