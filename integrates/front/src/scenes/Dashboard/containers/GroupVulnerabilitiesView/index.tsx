import { useQuery } from "@apollo/client";
import type { ColumnDef } from "@tanstack/react-table";
import React from "react";
import { useParams } from "react-router-dom";

import { GET_GROUP_VULNERABILITIES } from "./queries";
import type { IGroupVulnerabilities, IVulnerability } from "./types";

import { Table } from "components/TableNew";
import { formatLinkHandler } from "components/TableNew/formatters/linkFormatter";
import { useDebouncedCallback } from "utils/hooks";

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

const GroupVulnerabilitiesView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const { data, refetch } = useQuery<IGroupVulnerabilities>(
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

  const handleSearch = useDebouncedCallback((search: string): void => {
    void refetch({ search });
  }, 500);

  return (
    <div>
      <Table
        columns={tableColumns}
        data={vulnerabilities}
        exportCsv={false}
        id={"tblGroupVulnerabilities"}
        onSearch={handleSearch}
      />
    </div>
  );
};

export { GroupVulnerabilitiesView };
