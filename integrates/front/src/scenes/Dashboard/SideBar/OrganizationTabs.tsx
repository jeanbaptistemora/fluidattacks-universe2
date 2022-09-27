/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */
import {
  faChartColumn,
  faFileLines,
  faFolder,
  faShield,
} from "@fortawesome/free-solid-svg-icons";
import React, { Fragment } from "react";
import type { FC } from "react";
import { Route, useParams } from "react-router-dom";

import { GroupTabs } from "./GroupTabs";

import { SideBarSubTabs, SideBarTab } from "components/SideBar";

const OrganizationTabs: FC = (): JSX.Element => {
  const { org } = useParams<{ org: string }>();

  return (
    <Fragment>
      <SideBarSubTabs>
        <SideBarTab icon={faFolder} to={`/orgs/${org}/groups`}>
          {"Groups"}
        </SideBarTab>
        <Route path={"/orgs/:org/groups/:group/"}>
          <GroupTabs />
        </Route>
      </SideBarSubTabs>
      <SideBarTab icon={faChartColumn} to={`/orgs/${org}/analytics`}>
        {"Analytics"}
      </SideBarTab>
      <SideBarTab icon={faShield} to={`/orgs/${org}/policies`}>
        {"Policies"}
      </SideBarTab>
      <SideBarTab icon={faFileLines} to={`/orgs/${org}/compliance`}>
        {"Compliance"}
      </SideBarTab>
    </Fragment>
  );
};

export { OrganizationTabs };
