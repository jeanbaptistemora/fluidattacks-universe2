/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import type { ITableLinkProps } from ".";
import { TableLink } from ".";

const config: Meta = {
  component: TableLink,
  title: "components/TableLink",
};

const Template: Story<ITableLinkProps> = (props): JSX.Element => (
  <MemoryRouter>
    <TableLink {...props} />
  </MemoryRouter>
);

const Default = Template.bind({});
Default.args = {
  to: "Home",
  value: "Test message",
};

export { Default };
export default config;
