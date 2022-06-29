/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { IItemProps, IListProps } from ".";
import { List } from ".";
import { Button } from "components/Button";

const config: Meta = {
  component: List,
  title: "components/List",
};

const Template: Story<IListProps> = (props): JSX.Element => <List {...props} />;

const Default = Template.bind({});
Default.args = {
  columns: 2,
  height: "300px",
  items: [...Array(15).keys()].map(
    (id: number): IItemProps => ({
      id,
      text: `Element ${id}`,
    })
  ),
  render: (el: IItemProps): JSX.Element => (
    <Button variant={"basic"}>{el.text}</Button>
  ),
};

export { Default };
export default config;
