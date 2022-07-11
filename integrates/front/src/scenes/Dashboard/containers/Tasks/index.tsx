import React from "react";
import { useTranslation } from "react-i18next";
import { MemoryRouter, Route, Switch, useRouteMatch } from "react-router-dom";

import { Tab, Tabs } from "components/Tabs";
import { TasksDrafts } from "scenes/Dashboard/containers/Tasks/TasksDrafts";
import { TasksVulnerabilities } from "scenes/Dashboard/containers/Tasks/TasksVulnerabilities";
import type { ITasksContent } from "scenes/Dashboard/containers/Tasks/types";
import { TabContent } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import {
  authzPermissionsContext,
  userLevelPermissions,
} from "utils/authz/config";

export const TasksContent: React.FC<ITasksContent> = ({
  userData,
  meVulnerabilitiesAssigned,
  setUserRole,
  refetchVulnerabilitiesAssigned,
}: ITasksContent): JSX.Element => {
  const { t } = useTranslation();
  const { path, url } = useRouteMatch<{ path: string; url: string }>();

  return (
    <React.StrictMode>
      <p className={"f3 fw7 mt4 mb3"}>{t("todoList.title")}</p>
      <MemoryRouter initialEntries={[`${url}/vulns`]} initialIndex={0}>
        <Tabs>
          <Tab
            id={"tasksVulnerabilities"}
            link={`${url}/vulns`}
            tooltip={t("todoList.tooltip.vulnerabilities")}
          >
            {t("todoList.tabs.vulnerabilities")}
          </Tab>
          <authzPermissionsContext.Provider value={userLevelPermissions}>
            <Can do={"front_can_retrieve_todo_drafts"}>
              <Tab
                id={"tasksVulnerabilities"}
                link={`${url}/drafts`}
                tooltip={t("todoList.tooltip.drafts")}
              >
                {t("todoList.tabs.drafts")}
              </Tab>
            </Can>
          </authzPermissionsContext.Provider>
        </Tabs>
        <TabContent>
          <Switch>
            <Route exact={true} path={`${path}/vulns`}>
              <TasksVulnerabilities
                meVulnerabilitiesAssigned={meVulnerabilitiesAssigned}
                refetchVulnerabilitiesAssigned={refetchVulnerabilitiesAssigned}
                setUserRole={setUserRole}
                userData={userData}
              />
            </Route>
            <Route exact={true} path={`${path}/drafts`}>
              <TasksDrafts />
            </Route>
          </Switch>
        </TabContent>
      </MemoryRouter>
    </React.StrictMode>
  );
};
