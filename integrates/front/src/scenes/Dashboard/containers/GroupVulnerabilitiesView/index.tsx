/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useQuery } from "@apollo/client";
import type { ColumnDef } from "@tanstack/react-table";
import React, { useCallback } from "react";
import { useParams } from "react-router-dom";

import { GET_GROUP_VULNERABILITIES } from "./queries";
import type { IGroupVulnerabilities, IVulnerability } from "./types";

import { formatState } from "../GroupFindingsView/utils";
import { Table } from "components/TableNew";
import { formatLinkHandler } from "components/TableNew/formatters/linkFormatter";
import { formatTreatment } from "utils/formatHelpers";
import { useDebouncedCallback } from "utils/hooks";

const tableColumns: ColumnDef<IVulnerability>[] = [
  {
    accessorFn: (row): string => `${row.where} | ${row.specific}`,
    enableColumnFilter: false,
    header: "Vulnerability",
  },
  {
    accessorFn: (row): string => row.finding.title,
    cell: (cell): JSX.Element => {
      const link = `vulns/${cell.row.original.finding.id}/description`;
      const text = cell.getValue<string>();

      return formatLinkHandler(link, text);
    },
    header: "Type",
    meta: { filterType: "select" },
  },
  {
    accessorKey: "currentState",
    cell: (cell): JSX.Element => formatState(cell.getValue()),
    header: "Status",
    meta: { filterType: "select" },
  },
  {
    accessorKey: "treatment",
    cell: (cell): string =>
      formatTreatment(cell.getValue(), cell.row.original.currentState),
    header: "Treatment",
    meta: { filterType: "select" },
  },
  {
    accessorKey: "verification",
    header: "Reattack",
    meta: { filterType: "select" },
  },

  {
    accessorKey: "reportDate",
    enableColumnFilter: false,
    header: "Found",
    meta: { filterType: "dateRange" },
  },
  {
    accessorFn: (row): number => row.finding.severityScore,
    cell: (cell): JSX.Element => {
      const link = `${cell.row.original.finding.id}/severity`;
      const text = cell.getValue<string>();

      return formatLinkHandler(link, text);
    },
    header: "Severity",
    meta: { filterType: "numberRange" },
  },
  {
    accessorFn: (): string => "View",
    cell: (cell): JSX.Element => {
      const link = `${cell.row.original.finding.id}/evidence`;
      const text = cell.getValue<string>();

      return formatLinkHandler(link, text);
    },
    enableColumnFilter: false,
    header: "Evidence",
  },
];

const GroupVulnerabilitiesView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const { data, fetchMore, refetch } = useQuery<IGroupVulnerabilities>(
    GET_GROUP_VULNERABILITIES,
    {
      fetchPolicy: "cache-first",
      variables: { first: 100, groupName, search: "" },
    }
  );
  const vulnerabilities =
    data === undefined
      ? []
      : data.group.vulnerabilities.edges.map(
          (edge): IVulnerability => edge.node
        );

  const handleNextPage = useCallback(async (): Promise<void> => {
    const pageInfo =
      data === undefined
        ? { endCursor: "", hasNextPage: false }
        : data.group.vulnerabilities.pageInfo;

    if (pageInfo.hasNextPage) {
      await fetchMore({ variables: { after: pageInfo.endCursor } });
    }
  }, [data, fetchMore]);

  const handleSearch = useDebouncedCallback((search: string): void => {
    void refetch({ search });
  }, 500);

  return (
    <div>
      <Table
        columnToggle={true}
        columns={tableColumns}
        data={vulnerabilities}
        enableColumnFilters={true}
        exportCsv={false}
        id={"tblGroupVulnerabilities"}
        onNextPage={handleNextPage}
        onSearch={handleSearch}
      />
    </div>
  );
};

export { GroupVulnerabilitiesView };
