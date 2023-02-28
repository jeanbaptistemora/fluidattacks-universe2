import { useQuery } from "@apollo/client";
import type { ColumnDef, Row } from "@tanstack/react-table";
import _ from "lodash";
import React, { useCallback, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";

import { formatDrafts } from "./utils";

import type { IFilter } from "components/Filter";
import { Filters, useFilters } from "components/Filter";
import { Table } from "components/Table";
import { filterDate } from "components/Table/filters/filterFunctions/filterDate";
import type { ICellHelper } from "components/Table/types";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import { GET_TODO_DRAFTS } from "scenes/Dashboard/containers/Tasks-Content/Drafts/queries";
import type {
  IGetTodoDrafts,
  ITodoDraftAttr,
} from "scenes/Dashboard/containers/Tasks-Content/Drafts/types";
import { GET_USER_ORGANIZATIONS_GROUPS } from "scenes/Dashboard/queries";
import type { IGetUserOrganizationsGroups } from "scenes/Dashboard/types";
import { Logger } from "utils/logger";

export const TasksDrafts: React.FC = (): JSX.Element => {
  const { push } = useHistory();
  const { t } = useTranslation();

  const hackerFormatter = (value: string): JSX.Element => {
    return <div className={`tl truncate`}>{value}</div>;
  };

  const columns: ColumnDef<ITodoDraftAttr>[] = [
    {
      accessorKey: "reportDate",
      filterFn: filterDate,
      header: "Date",
    },
    {
      accessorKey: "title",
      header: "Type",
    },
    {
      accessorKey: "severityScore",
      header: "Severity",
    },
    {
      accessorKey: "openVulnerabilities",
      header: "Open Vulns.",
    },
    {
      accessorKey: "groupName",
      header: "Group Name",
    },
    {
      accessorKey: "organizationName",
      header: t("todoList.tabs.drafts.organization"),
    },
    {
      accessorKey: "hacker",
      cell: (cell: ICellHelper<ITodoDraftAttr>): JSX.Element =>
        hackerFormatter(cell.getValue()),
      header: "Hacker",
    },
    {
      accessorKey: "currentState",
      cell: (cell: ICellHelper<ITodoDraftAttr>): JSX.Element =>
        statusFormatter(cell.getValue()),
      header: "State",
    },
    {
      accessorKey: "lastStateDate",
      header: t("todoList.tabs.drafts.stateDate"),
    },
  ];

  const [filters, setFilters] = useState<IFilter<ITodoDraftAttr>[]>([
    {
      id: "currentState",
      key: "currentState",
      label: "State",
      selectOptions: ["Created", "Rejected", "Submitted"],
      type: "select",
    },
  ]);

  const { data: userData } = useQuery<IGetUserOrganizationsGroups>(
    GET_USER_ORGANIZATIONS_GROUPS,
    {
      fetchPolicy: "cache-first",
      onError: ({ graphQLErrors }): void => {
        graphQLErrors.forEach((error): void => {
          Logger.warning("An error occurred fetching user groups", error);
        });
      },
    }
  );

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

  const drafts: ITodoDraftAttr[] = useMemo(
    (): ITodoDraftAttr[] =>
      formatDrafts(
        _.isNil(data) ? [] : data.me.drafts,
        userData === undefined ? [] : userData.me.organizations
      ),
    [data, userData]
  );

  const filteredDataset = useFilters(drafts, filters);

  const goToDraft = useCallback(
    (rowInfo: Row<ITodoDraftAttr>): ((event: React.FormEvent) => void) => {
      return (event: React.FormEvent): void => {
        push(
          `/groups/${rowInfo.original.groupName}/drafts/${rowInfo.original.id}/locations`
        );
        event.preventDefault();
      };
    },
    [push]
  );

  return (
    <React.StrictMode>
      <Table
        columns={columns}
        data={filteredDataset}
        exportCsv={true}
        filters={<Filters filters={filters} setFilters={setFilters} />}
        id={"tblTodoDrafts"}
        onRowClick={goToDraft}
      />
    </React.StrictMode>
  );
};
