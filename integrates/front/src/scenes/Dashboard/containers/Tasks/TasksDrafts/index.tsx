import { useQuery } from "@apollo/client";
import _ from "lodash";
import React from "react";
import type { SortOrder } from "react-bootstrap-table-next";

import { Table } from "components/Table";
import type { IHeaderConfig } from "components/Table/types";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import { GET_TODO_DRAFTS } from "scenes/Dashboard/containers/Tasks/TasksDrafts/queries";
import type {
  IGetTodoDrafts,
  ITodoDraftAttr,
  ITodoGroupAttr,
  ITodoOrganizationAttr,
} from "scenes/Dashboard/containers/Tasks/TasksDrafts/types";
import { Logger } from "utils/logger";

export const TasksDrafts: React.FC = (): JSX.Element => {
  const onSortState: (dataField: string, order: SortOrder) => void = (
    dataField: string,
    order: SortOrder
  ): void => {
    const newSorted = { dataField, order };
    sessionStorage.setItem("userDraftSort", JSON.stringify(newSorted));
  };

  const hackerFormatter = (value: string): JSX.Element => {
    return <span className={`black tl truncate`}>{value}</span>;
  };

  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "reportDate",
      header: "Date",
      onSort: onSortState,
      width: "10%",
    },

    {
      dataField: "title",
      header: "Type",
      onSort: onSortState,
      width: "30%",
      wrapped: true,
    },
    {
      dataField: "severityScore",
      header: "Severity",
      onSort: onSortState,
      width: "10%",
    },
    {
      dataField: "openVulnerabilities",
      header: "Open Vulns.",
      onSort: onSortState,
      width: "10%",
    },
    {
      dataField: "groupName",
      header: "Group Name",
      onSort: onSortState,
      width: "10%",
    },
    {
      dataField: "hacker",
      formatter: hackerFormatter,
      header: "Hacker",
      onSort: onSortState,
      width: "10%",
    },
    {
      dataField: "currentState",
      formatter: statusFormatter,
      header: "State",
      onSort: onSortState,
      width: "10%",
      wrapped: true,
    },
  ];

  const { data } = useQuery<IGetTodoDrafts>(GET_TODO_DRAFTS, {
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        Logger.warning(
          "An error occurred fetching user drafts from dashboard",
          error
        );
      });
    },
  });

  const dataset: ITodoDraftAttr[] =
    _.isUndefined(data) || _.isEmpty(data)
      ? []
      : _.flatten(
          data.me.organizations.map(
            (org: ITodoOrganizationAttr): ITodoDraftAttr[] =>
              _.flatten(
                org.groups.map(
                  (group: ITodoGroupAttr): ITodoDraftAttr[] => group.drafts
                )
              )
          )
        );

  return (
    <React.StrictMode>
      <Table
        dataset={dataset}
        exportCsv={false}
        headers={tableHeaders}
        id={"tblUserDrafts"}
        pageSize={25}
        search={false}
      />
    </React.StrictMode>
  );
};
