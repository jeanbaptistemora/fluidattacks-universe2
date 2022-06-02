import React from "react";
import {
  Redirect,
  Route,
  Switch,
  useParams,
  useRouteMatch,
} from "react-router-dom";

import { useGroupVulnerabilities } from "./hooks";
import type { IVulnerability } from "./types";
import {
  filterByState,
  filterByTreatment,
  formatEvidence,
  formatLocation,
} from "./utils";

import { Table } from "components/Table";
import { linkFormatter } from "components/Table/formatters";
import type { IHeaderConfig } from "components/Table/types";
import { ContentTab } from "scenes/Dashboard/components/ContentTab";
import { TabContent, TabsContainer } from "styles/styledComponents";

const tableHeaders: IHeaderConfig[] = [
  {
    dataField: "where",
    formatter: formatLocation,
    header: "Location",
    wrapped: true,
  },
  {
    dataField: "finding.title",
    formatter: linkFormatter<IVulnerability>(
      (_cell, row): string => `${row.finding.id}/description`
    ),
    header: "Type",
    wrapped: true,
  },
  {
    dataField: "reportDate",
    header: "Found",
  },
  {
    dataField: "finding.severityScore",
    formatter: linkFormatter<IVulnerability>(
      (_cell, row): string => `${row.finding.id}/severity`
    ),
    header: "Severity",
  },
  {
    dataField: "evidence",
    formatter: formatEvidence,
    header: "Evidence",
  },
];

const views = [
  { filter: filterByState("open"), title: "Open" },
  { filter: filterByState("closed"), title: "Closed" },
  {
    filter: filterByTreatment("ACCEPTED"),
    title: "Temporarily accepted",
  },
  {
    filter: filterByTreatment("ACCEPTED_UNDEFINED"),
    title: "Permanently accepted",
  },
];

const GroupVulnerabilitiesView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const { path, url } = useRouteMatch();
  const vulnerabilities = useGroupVulnerabilities(groupName);

  return (
    <div>
      <TabsContainer>
        {views.map(({ title }): JSX.Element => {
          return (
            <ContentTab
              id={`${title}VulnerabilitiesTab`}
              key={title}
              link={`${url}/${title}`}
              title={title}
              tooltip={""}
            />
          );
        })}
      </TabsContainer>
      <TabContent>
        <Switch>
          {views.map(({ title, filter }): JSX.Element => {
            return (
              <Route exact={true} key={title} path={`${path}/${title}`}>
                <Table
                  dataset={vulnerabilities.filter(filter)}
                  exportCsv={false}
                  headers={tableHeaders}
                  id={`tblVulnerabilities${title}`}
                  pageSize={10}
                  search={false}
                />
              </Route>
            );
          })}
          <Redirect to={`${path}/Open`} />
        </Switch>
      </TabContent>
    </div>
  );
};

export { GroupVulnerabilitiesView };
