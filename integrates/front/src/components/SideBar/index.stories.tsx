/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import {
  faBell,
  faChartSimple,
  faHome,
} from "@fortawesome/free-solid-svg-icons";
import type { Meta, Story } from "@storybook/react";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { SideBar, SideBarSubTabs, SideBarTab } from ".";

const config: Meta = {
  component: SideBar,
  title: "components/SideBar",
};

const Default: Story = (): JSX.Element => (
  <div className={"vh-50 pl5"}>
    <MemoryRouter initialEntries={["/home"]}>
      <SideBar>
        <SideBarTab icon={faHome} to={"/home"}>
          {"Home"}
        </SideBarTab>
        <SideBarSubTabs>
          <SideBarTab key={"groups"} to={"/groups"}>
            {"Groups"}
          </SideBarTab>
          <SideBarTab key={"vulns"} to={"/vulns"}>
            {"Vulnerabilities"}
          </SideBarTab>
          <SideBarTab key={"locs"} to={"/locations"}>
            {"Locations"}
          </SideBarTab>
        </SideBarSubTabs>
        <SideBarTab icon={faChartSimple} to={"/analytics"}>
          {"Analytics"}
        </SideBarTab>
        <SideBarTab icon={faBell} to={"/alerts"}>
          {"Alerts"}
        </SideBarTab>
      </SideBar>
    </MemoryRouter>
  </div>
);

export { Default };
export default config;
