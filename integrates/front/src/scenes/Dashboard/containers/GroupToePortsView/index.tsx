/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type {
  ColumnDef,
  Row,
  SortingState,
  VisibilityState,
} from "@tanstack/react-table";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import moment from "moment";
import React, { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { Filters, useFilters } from "components/Filter";
import type { IFilter } from "components/Filter";
import { Table } from "components/Table";
import { filterDate } from "components/Table/filters/filterFunctions/filterDate";
import type { ICellHelper } from "components/Table/types";
import { GET_TOE_PORTS } from "scenes/Dashboard/containers/GroupToePortsView/queries";
import type {
  IGroupToePortsViewProps,
  IToePortAttr,
  IToePortData,
  IToePortEdge,
  IToePortsConnection,
} from "scenes/Dashboard/containers/GroupToePortsView/types";
import { authzPermissionsContext } from "utils/authz/config";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";

const NOSEENFIRSTTIMEBY = "no seen first time by";

const GroupToePortsView: React.FC<IGroupToePortsViewProps> = ({
  isInternal,
}: IGroupToePortsViewProps): JSX.Element => {
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canGetAttackedAt: boolean = permissions.can(
    "api_resolvers_toe_port_attacked_at_resolve"
  );
  const canGetAttackedBy: boolean = permissions.can(
    "api_resolvers_toe_port_attacked_by_resolve"
  );
  const canGetBePresentUntil: boolean = permissions.can(
    "api_resolvers_toe_port_be_present_until_resolve"
  );
  const canGetFirstAttackAt: boolean = permissions.can(
    "api_resolvers_toe_port_first_attack_at_resolve"
  );
  const canGetSeenFirstTimeBy: boolean = permissions.can(
    "api_resolvers_toe_port_seen_first_time_by_resolve"
  );
  const canUpdateToePort: boolean = permissions.can(
    "api_mutations_update_toe_port_mutate"
  );

  const { groupName } = useParams<{ groupName: string }>();
  const [selectedToePortDatas, setSelectedToePortDatas] = useState<
    IToePortData[]
  >([]);

  const [columnVisibility, setColumnVisibility] =
    useStoredState<VisibilityState>(
      "tblToePorts-visibilityState",
      {
        address: false,
        attackedAt: true,
        attackedBy: false,
        bePresent: false,
        bePresentUntil: false,
        firstAttackAt: false,
        hasVulnerabilities: true,
        port: true,
        rootNickname: true,
        seenAt: true,
        seenFirstTimeBy: true,
      },
      localStorage
    );
  const [sorting, setSorting] = useStoredState<SortingState>(
    "tblToePorts-sortingState",
    []
  );

  // // GraphQL operations
  const getToePortsVariables = {
    canGetAttackedAt,
    canGetAttackedBy,
    canGetBePresentUntil,
    canGetFirstAttackAt,
    canGetSeenFirstTimeBy,
    groupName,
  };
  const { data, fetchMore, refetch } = useQuery<{
    group: { toePorts: IToePortsConnection };
  }>(GET_TOE_PORTS, {
    fetchPolicy: "network-only",
    nextFetchPolicy: "cache-first",
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load toe ports", error);
      });
    },
    variables: {
      ...getToePortsVariables,
      first: 150,
    },
  });
  const pageInfo =
    data === undefined ? undefined : data.group.toePorts.pageInfo;
  const toePortsEdges: IToePortEdge[] =
    data === undefined ? [] : data.group.toePorts.edges;
  const formatOptionalDate: (date: string | null) => Date | undefined = (
    date: string | null
  ): Date | undefined => (_.isNull(date) ? undefined : new Date(date));
  const markSeenFirstTimeBy: (seenFirstTimeBy: string) => string = (
    seenFirstTimeBy: string
  ): string =>
    _.isEmpty(seenFirstTimeBy) ? NOSEENFIRSTTIMEBY : seenFirstTimeBy;
  const formatToePortData: (toePortAttr: IToePortAttr) => IToePortData = (
    toePortAttr: IToePortAttr
  ): IToePortData => ({
    ...toePortAttr,
    attackedAt: formatOptionalDate(toePortAttr.attackedAt),
    bePresentUntil: formatOptionalDate(toePortAttr.bePresentUntil),
    firstAttackAt: formatOptionalDate(toePortAttr.firstAttackAt),
    markedSeenFirstTimeBy: markSeenFirstTimeBy(toePortAttr.seenFirstTimeBy),
    rootId: _.isNil(toePortAttr.root) ? "" : toePortAttr.root.id,
    rootNickname: _.isNil(toePortAttr.root) ? "" : toePortAttr.root.nickname,
    seenAt: formatOptionalDate(toePortAttr.seenAt),
  });
  const toePorts: IToePortData[] = toePortsEdges.map(
    ({ node }): IToePortData => formatToePortData(node)
  );

  const formatBoolean = (value: boolean): string =>
    value ? t("group.toe.ports.yes") : t("group.toe.ports.no");
  const formatDate: (date: Date | undefined) => string = (
    date: Date | undefined
  ): string => {
    if (_.isUndefined(date)) {
      return "";
    }

    return moment(date).format("YYYY-MM-DD");
  };

  const columns: ColumnDef<IToePortData>[] = [
    {
      accessorKey: "rootNickname",
      header: t("group.toe.ports.root"),
      meta: { filterType: "select" },
    },
    {
      accessorKey: "address",
      header: t("group.toe.ports.address"),
      meta: { filterType: "select" },
    },
    {
      accessorKey: "port",
      header: t("group.toe.ports.port"),
    },
    {
      accessorFn: (row: IToePortData): string => {
        return formatBoolean(row.hasVulnerabilities);
      },
      header: String(t("group.toe.ports.hasVulnerabilities")),
      meta: { filterType: "select" },
    },
    {
      accessorKey: "seenAt",
      cell: (cell: ICellHelper<IToePortData>): string =>
        formatDate(cell.getValue()),
      filterFn: filterDate,
      header: t("group.toe.ports.seenAt"),
      meta: { filterType: "dateRange" },
    },
    {
      accessorFn: (row: IToePortData): string => {
        return formatBoolean(row.bePresent);
      },
      header: t("group.toe.ports.bePresent"),
      id: "bePresent",
      meta: { filterType: "select" },
    },
    {
      accessorKey: "attackedAt",
      cell: (cell: ICellHelper<IToePortData>): string =>
        formatDate(cell.getValue()),
      filterFn: filterDate,
      header: t("group.toe.ports.attackedAt"),
      id: "attackedAt",
      meta: { filterType: "dateRange" },
    },
    {
      accessorKey: "attackedBy",
      header: t("group.toe.ports.attackedBy"),
      id: "attackedBy",
    },
    {
      accessorKey: "firstAttackAt",
      cell: (cell: ICellHelper<IToePortData>): string =>
        formatDate(cell.getValue()),
      filterFn: filterDate,
      header: t("group.toe.ports.firstAttackAt"),
      id: "firstAttackAt",
      meta: { filterType: "dateRange" },
    },
    {
      accessorKey: "seenFirstTimeBy",
      header: t("group.toe.ports.seenFirstTimeBy"),
      id: "seenFirstTimeBy",
    },
    {
      accessorKey: "bePresentUntil",
      cell: (cell: ICellHelper<IToePortData>): string =>
        formatDate(cell.getValue()),
      filterFn: filterDate,
      header: t("group.toe.ports.bePresentUntil"),
      id: "bePresentUntil",
      meta: { filterType: "dateRange" },
    },
  ];

  const baseFilters: IFilter<IToePortData>[] = [
    {
      id: "rootNickname",
      key: "rootNickname",
      label: t("group.toe.ports.root"),
      selectOptions: (ports): string[] =>
        [
          ...new Set(ports.map((datapoint): string => datapoint.rootNickname)),
        ].filter(Boolean),
      type: "select",
    },
    {
      id: "address",
      key: "address",
      label: t("group.toe.ports.address"),
      selectOptions: (ports): string[] =>
        [
          ...new Set(ports.map((datapoint): string => datapoint.address)),
        ].filter(Boolean),
      type: "select",
    },
    {
      id: "port",
      key: "port",
      label: t("group.toe.ports.port"),
      type: "text",
    },
    {
      id: "hasVulnerabilities",
      key: "hasVulnerabilities",
      label: t("group.toe.ports.hasVulnerabilities"),
      selectOptions: [
        { header: formatBoolean(true), value: "true" },
        { header: formatBoolean(false), value: "false" },
      ],
      type: "select",
    },
    {
      id: "seenAt",
      key: "seenAt",
      label: t("group.toe.ports.seenAt"),
      type: "dateRange",
    },
    {
      id: "bePresent",
      key: "bePresent",
      label: t("group.toe.ports.bePresent"),
      selectOptions: [
        { header: formatBoolean(true), value: "true" },
        { header: formatBoolean(false), value: "false" },
      ],
      type: "select",
    },
    {
      id: "attackedAt",
      key: "attackedAt",
      label: t("group.toe.ports.attackedAt"),
      type: "dateRange",
    },
    {
      id: "attackedBy",
      key: "attackedBy",
      label: t("group.toe.ports.attackedBy"),
      type: "text",
    },
    {
      id: "firstAttackAt",
      key: "firstAttackAt",
      label: t("group.toe.ports.firstAttackAt"),
      type: "dateRange",
    },
    {
      id: "seenFirstTimeBy",
      key: "seenFirstTimeBy",
      label: t("group.toe.ports.seenFirstTimeBy"),
      type: "text",
    },
    {
      id: "bePresentUntil",
      key: "bePresentUntil",
      label: t("group.toe.ports.bePresentUntil"),
      type: "dateRange",
    },
  ];

  const tableColumns = columns.filter((column): boolean => {
    switch (column.id) {
      case "attackedAt":
        return isInternal && canGetAttackedAt;
      case "attackedBy":
        return isInternal && canGetAttackedBy;
      case "firstAttackAt":
        return isInternal && canGetFirstAttackAt;
      case "seenFirstTimeBy":
        return isInternal && canGetSeenFirstTimeBy;
      case "bePresentUntil":
        return isInternal && canGetBePresentUntil;
      default:
        return true;
    }
  });

  const tableFilters = baseFilters.filter((filter): boolean => {
    switch (filter.id) {
      case "attackedAt":
        return isInternal && canGetAttackedAt;
      case "attackedBy":
        return isInternal && canGetAttackedBy;
      case "firstAttackAt":
        return isInternal && canGetFirstAttackAt;
      case "seenFirstTimeBy":
        return isInternal && canGetSeenFirstTimeBy;
      case "bePresentUntil":
        return isInternal && canGetBePresentUntil;
      default:
        return true;
    }
  });

  const [filters, setFilters] = useState<IFilter<IToePortData>[]>(tableFilters);

  const filteredToeLines = useFilters(toePorts, filters);

  useEffect((): void => {
    if (!_.isUndefined(pageInfo)) {
      if (pageInfo.hasNextPage) {
        void fetchMore({
          variables: { after: pageInfo.endCursor, first: 1200 },
        });
      }
    }
  }, [pageInfo, fetchMore]);
  useEffect((): void => {
    setSelectedToePortDatas([]);
    void refetch();
  }, [refetch]);

  function enabledRows(row: Row<IToePortData>): boolean {
    return row.original.bePresent;
  }

  return (
    <React.StrictMode>
      <Table
        columnToggle={true}
        columnVisibilitySetter={setColumnVisibility}
        columnVisibilityState={columnVisibility}
        columns={tableColumns}
        data={filteredToeLines}
        enableRowSelection={enabledRows}
        exportCsv={true}
        extraButtons={undefined}
        filters={
          <Filters
            dataset={toePorts}
            filters={filters}
            setFilters={setFilters}
          />
        }
        id={"tblToePorts"}
        rowSelectionSetter={
          !isInternal || !canUpdateToePort ? undefined : setSelectedToePortDatas
        }
        rowSelectionState={selectedToePortDatas}
        sortingSetter={setSorting}
        sortingState={sorting}
      />
    </React.StrictMode>
  );
};

export { GroupToePortsView };
