/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";
import { useTranslation } from "react-i18next";
import { Redirect, Route, Switch, useRouteMatch } from "react-router-dom";

import { OrganizationComplianceOverviewView } from "../OrganizationComplianceOverviewView";
import { Tab, Tabs } from "components/Tabs";
import { TabContent } from "styles/styledComponents";

const ComplianceContent: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { path, url } = useRouteMatch<{ path: string; url: string }>();

  return (
    <React.StrictMode>
      <Tabs>
        <Tab
          id={"overviewTab"}
          link={`${url}/overview`}
          tooltip={t("organization.tabs.compliance.tabs.overview.tooltip")}
        >
          {t("organization.tabs.compliance.tabs.overview.text")}
        </Tab>
      </Tabs>
      <TabContent>
        <Switch>
          <Route exact={true} path={`${path}/overview`}>
            <OrganizationComplianceOverviewView organizationId={"okada"} />
          </Route>
          <Redirect to={`${path}/overview`} />
        </Switch>
      </TabContent>
    </React.StrictMode>
  );
};

export { ComplianceContent };
