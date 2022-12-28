import React from "react";
import { useTranslation } from "react-i18next";
import { Redirect, Route, Switch, useRouteMatch } from "react-router-dom";

import { OrganizationComplianceOverviewView } from "./OrganizationComplianceOverviewView";
import { OrganizationComplianceStandardsView } from "./OrganizationComplianceStandardsView";
import type { IComplianceContentProps } from "./types";

import { Tab, Tabs } from "components/Tabs";
import { TabContent } from "styles/styledComponents";

const ComplianceContent: React.FC<IComplianceContentProps> = (
  props: IComplianceContentProps
): JSX.Element => {
  const { organizationId } = props;
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
        <Tab
          id={"standardsTab"}
          link={`${url}/standards`}
          tooltip={t("organization.tabs.compliance.tabs.standards.tooltip")}
        >
          {t("organization.tabs.compliance.tabs.standards.text")}
        </Tab>
      </Tabs>
      <TabContent>
        <Switch>
          <Route exact={true} path={`${path}/overview`}>
            <OrganizationComplianceOverviewView
              organizationId={organizationId}
            />
          </Route>
          <Route exact={true} path={`${path}/standards`}>
            <OrganizationComplianceStandardsView
              organizationId={organizationId}
            />
          </Route>
          <Redirect to={`${path}/overview`} />
        </Switch>
      </TabContent>
    </React.StrictMode>
  );
};

export { ComplianceContent };
