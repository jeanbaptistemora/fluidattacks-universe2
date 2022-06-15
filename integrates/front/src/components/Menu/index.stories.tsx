/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";
import { Link, MemoryRouter } from "react-router-dom";

import { Menu, MenuDivider, MenuItem } from ".";

const config: Meta = {
  component: Menu,
  parameters: { docs: { iframeHeight: 200, inlineStories: false } },
  subcomponents: { MenuDivider, MenuItem },
  title: "components/Menu",
};

const Default: Story = (): JSX.Element => (
  <MemoryRouter>
    <Menu align={"left"}>
      <MenuItem>
        <Link to={"/profile"}>{"Profile"}</Link>
      </MenuItem>
      <MenuItem>
        <button>{"Delete account"}</button>
      </MenuItem>
      <MenuDivider />
      <MenuItem>
        <Link to={"/logout"}>{"Log out"}</Link>
      </MenuItem>
    </Menu>
  </MemoryRouter>
);

export { Default };
export default config;
