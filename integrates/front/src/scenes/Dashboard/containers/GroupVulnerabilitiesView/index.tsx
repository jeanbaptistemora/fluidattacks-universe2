import type { ColumnDef } from "@tanstack/react-table";
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
import { filterByState, filterByTreatment } from "./utils";

import { Tables } from "components/TableNew";
import { formatLinkHandler } from "components/TableNew/formatters/linkFormatter";
import { Tab, Tabs } from "components/Tabs";
import { TabContent } from "styles/styledComponents";

const tableColumns: ColumnDef<IVulnerability>[] = [
  {
    accessorFn: (row): string => `${row.where} | ${row.specific}`,
    header: "Vulnerability",
  },
  {
    accessorFn: (row): string => row.finding.title,
    cell: (cell): JSX.Element => {
      const link = `${cell.row.original.finding.id}/description`;
      const text = cell.getValue<string>();

      return formatLinkHandler(link, text);
    },
    header: "Type",
  },
  {
    accessorKey: "reportDate",
    header: "Found",
  },
  {
    accessorFn: (row): string => row.finding.severityScore.toString(),
    cell: (cell): JSX.Element => {
      const link = `${cell.row.original.finding.id}/severity`;
      const text = cell.getValue<string>();

      return formatLinkHandler(link, text);
    },
    header: "Severity",
  },
  {
    accessorFn: (): string => "View",
    cell: (cell): JSX.Element => {
      const link = `${cell.row.original.finding.id}/evidence`;
      const text = cell.getValue<string>();

      return formatLinkHandler(link, text);
    },
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
  const vulnerabilities = useGroupVulnerabilities(groupName, "");

  return (
    <div>
      <Tabs>
        {views.map(({ title }): JSX.Element => {
          return (
            <Tab
              id={`${title}VulnerabilitiesTab`}
              key={title}
              link={`${url}/${title}`}
              tooltip={""}
            >
              {title}
            </Tab>
          );
        })}
      </Tabs>
      <TabContent>
        <Switch>
          {views.map(({ title, filter }): JSX.Element => {
            return (
              <Route exact={true} key={title} path={`${path}/${title}`}>
                <Tables
                  columns={tableColumns}
                  data={vulnerabilities.filter(filter)}
                  exportCsv={false}
                  id={`tblVulnerabilities${title}`}
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
