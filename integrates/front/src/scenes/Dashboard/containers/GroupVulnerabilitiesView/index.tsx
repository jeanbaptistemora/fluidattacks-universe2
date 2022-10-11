/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint fp/no-mutation: 0 */
import { useQuery } from "@apollo/client";
import type { ColumnDef } from "@tanstack/react-table";
import React, { useCallback } from "react";
import { useParams } from "react-router-dom";

import { GET_GROUP_VULNERABILITIES } from "./queries";
import type { IGroupVulnerabilities } from "./types";

import type { IHistoricTreatment } from "../DescriptionView/types";
import { formatState } from "../GroupFindingsView/utils";
import { formatLinkHandler } from "components/TableNew/formatters/linkFormatter";
import { VulnComponent } from "scenes/Dashboard/components/Vulnerabilities";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { formatHistoricTreatment } from "scenes/Dashboard/components/Vulnerabilities/utils";
import { formatTreatment } from "utils/formatHelpers";
import { useDebouncedCallback } from "utils/hooks";

const tableColumns: ColumnDef<IVulnRowAttr>[] = [
  {
    accessorFn: (row): string => `${row.where} | ${row.specific}`,
    enableColumnFilter: false,
    header: "Vulnerability",
  },
  {
    accessorFn: (row): string => String(row.finding?.title),
    cell: (cell): JSX.Element => {
      const link = `vulns/${String(cell.row.original.finding?.id)}/description`;
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
    accessorFn: (row): number => Number(row.finding?.severityScore),
    cell: (cell): JSX.Element => {
      const link = `vulns/${String(cell.row.original.finding?.id)}/severity`;
      const text = cell.getValue<string>();

      return formatLinkHandler(link, text);
    },
    header: "Severity",
    meta: { filterType: "numberRange" },
  },
  {
    accessorFn: (): string => "View",
    cell: (cell): JSX.Element => {
      const link = `vulns/${String(cell.row.original.finding?.id)}/evidence`;
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
      : data.group.vulnerabilities.edges
          .map((edge): IVulnRowAttr => edge.node)
          .map((vulnerability): IVulnRowAttr => {
            const lastTreatment: IHistoricTreatment =
              formatHistoricTreatment(vulnerability);

            return {
              ...vulnerability,
              historicTreatment: [lastTreatment],
            };
          });

  const handleNextPage = useCallback(async (): Promise<void> => {
    const pageInfo =
      data === undefined
        ? { endCursor: "", hasNextPage: false }
        : data.group.vulnerabilities.pageInfo;

    if (pageInfo.hasNextPage) {
      await fetchMore({
        updateQuery: (
          previousResult,
          { fetchMoreResult }
        ): IGroupVulnerabilities => {
          if (!fetchMoreResult) {
            return previousResult;
          }

          const previousEdges = previousResult.group.vulnerabilities.edges;
          const fetchMoreEdges = fetchMoreResult.group.vulnerabilities.edges;

          fetchMoreResult.group.vulnerabilities.edges = [
            ...previousEdges,
            ...fetchMoreEdges,
          ];

          return { ...fetchMoreResult };
        },
        variables: { after: pageInfo.endCursor },
      });
    }
  }, [data, fetchMore]);

  const handleSearch = useDebouncedCallback((search: string): void => {
    void refetch({ search });
  }, 500);

  return (
    <div>
      <VulnComponent
        columnToggle={true}
        columns={tableColumns}
        isEditing={false}
        isRequestingReattack={false}
        isVerifyingRequest={false}
        onNextPage={handleNextPage}
        onSearch={handleSearch}
        refetchData={refetch}
        vulnerabilities={vulnerabilities}
      />
    </div>
  );
};

export { GroupVulnerabilitiesView };
