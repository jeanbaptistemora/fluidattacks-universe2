import React from "react";
import { useTranslation } from "react-i18next";

import { Tab, Tabs } from "components/Tabs";
import type { ITasksContent } from "scenes/Dashboard/containers/Tasks/types";
import { TasksVulnerabilities } from "scenes/Dashboard/containers/TasksVulnerabilities";
import { TabContent } from "styles/styledComponents";

export const TasksContent: React.FC<ITasksContent> = ({
  userData,
  meVulnerabilitiesAssigned,
  setUserRole,
  refetchVulnerabilitiesAssigned,
}: ITasksContent): JSX.Element => {
  const { t } = useTranslation();

  return (
    <React.StrictMode>
      <Tabs>
        <Tab
          id={"tasksVulnerabilities"}
          link={`/todos`}
          tooltip={t("todoList.tooltip.vulnerabilities")}
        >
          {t("todoList.tabs.vulnerabilities")}
        </Tab>
      </Tabs>
      <TabContent>
        <TasksVulnerabilities
          meVulnerabilitiesAssigned={meVulnerabilitiesAssigned}
          refetchVulnerabilitiesAssigned={refetchVulnerabilitiesAssigned}
          setUserRole={setUserRole}
          userData={userData}
        />
      </TabContent>
    </React.StrictMode>
  );
};
