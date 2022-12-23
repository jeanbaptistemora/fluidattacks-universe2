/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { IListProps } from ".";
import { List } from ".";
import { Button } from "components/Button";

const config: Meta = {
  component: List,
  title: "components/List",
};

const Template: Story<IListProps<number>> = (props): JSX.Element => (
  <List {...props} />
);

const Default = Template.bind({});
Default.args = {
  columns: 2,
  items: [...Array(15).keys()],
  render: (el: number): JSX.Element => <Button>{`Element ${el}`}</Button>,
};

export { Default };
export default config;
