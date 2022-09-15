/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */
import {
  faBell,
  faChartColumn,
  faCog,
  faFileLines,
  faHome,
  faShield,
} from "@fortawesome/free-solid-svg-icons";
import type { FC } from "react";
import React, { useContext } from "react";
import { Route, useParams } from "react-router-dom";

import { GroupTabs } from "./GroupTabs";

import { Sidebar } from "../components/Sidebar";
import { SideBar, SideBarTab } from "components/SideBar";
import { featurePreviewContext } from "utils/featurePreview";

const DashboardSideBar: FC = (): JSX.Element => {
  const { featurePreview } = useContext(featurePreviewContext);
  const { org } = useParams<{ org: string }>();

  const homeSubTabs = [
    <SideBarTab key={"groups"} to={`/orgs/${org}/groups`}>
      {"Groups"}
    </SideBarTab>,
    <Route key={"groupRoutes"} path={"/orgs/:org/groups/:group/"}>
      <GroupTabs />
    </Route>,
  ];

  return featurePreview ? (
    <SideBar>
      <SideBarTab icon={faHome} subTabs={homeSubTabs} to={"/home"}>
        {"Home"}
      </SideBarTab>
      <SideBarTab icon={faChartColumn} to={`/orgs/${org}/analytics`}>
        {"Analytics"}
      </SideBarTab>
      <SideBarTab disabled={true} icon={faBell} to={`/orgs/${org}/alerts`}>
        {"Alerts"}
      </SideBarTab>
      <SideBarTab icon={faShield} to={`/orgs/${org}/policies`}>
        {"Policies"}
      </SideBarTab>
      <SideBarTab
        disabled={true}
        icon={faFileLines}
        to={`/orgs/${org}/compliance`}
      >
        {"Compliance"}
      </SideBarTab>
      <SideBarTab disabled={true} icon={faCog} to={`/orgs/${org}/settings`}>
        {"Settings"}
      </SideBarTab>
    </SideBar>
  ) : (
    <Sidebar />
  );
};

export { DashboardSideBar };
