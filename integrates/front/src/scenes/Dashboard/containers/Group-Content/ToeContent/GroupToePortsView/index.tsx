import { useApolloClient, useMutation, useQuery } from "@apollo/client";
import type { ApolloError, FetchResult } from "@apollo/client";
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
import React, { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { ActionButtons } from "./ActionButtons";
import { editableBePresentFormatter } from "./formatters/editableBePresentFormatter";
import { HandleAdditionModal } from "./HandleAdditionModal";
import { isEqualRootId } from "./utils";

import { Filters, useFilters } from "components/Filter";
import type { IFilter } from "components/Filter";
import { Table } from "components/Table";
import { filterDate } from "components/Table/filters/filterFunctions/filterDate";
import type { ICellHelper } from "components/Table/types";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter";
import {
  GET_TOE_PORTS,
  UPDATE_TOE_PORT,
} from "scenes/Dashboard/containers/Group-Content/ToeContent/GroupToePortsView/queries";
import type {
  IGroupToePortsViewProps,
  IToePortAttr,
  IToePortData,
  IToePortEdge,
  IToePortsConnection,
  IUpdateToePortResultAttr,
} from "scenes/Dashboard/containers/Group-Content/ToeContent/GroupToePortsView/types";
import { authzPermissionsContext } from "utils/authz/config";
import { getErrors } from "utils/helpers";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const NOSEENFIRSTTIMEBY = "no seen first time by";

const GroupToePortsView: React.FC<IGroupToePortsViewProps> = ({
  isInternal,
}: IGroupToePortsViewProps): JSX.Element => {
  const { t } = useTranslation();
  const client = useApolloClient();

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
  const [isAdding, setIsAdding] = useState(false);
  const [isMarkingAsAttacked, setIsMarkingAsAttacked] = useState(false);
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
  const [handleUpdateToePort] = useMutation<IUpdateToePortResultAttr>(
    UPDATE_TOE_PORT,
    {
      onError: (errors: ApolloError): void => {
        errors.graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - The toe port is not present":
              msgError(t("group.toe.ports.alerts.nonPresent"));
              break;
            case "Exception - The toe port has been updated by another operation":
              msgError(t("group.toe.ports.alerts.alreadyUpdate"));
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning("An error occurred updating the toe port", error);
          }
        });
      },
    }
  );
  // eslint-disable-next-line react-hooks/exhaustive-deps
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

    // eslint-disable-next-line new-cap
    return Intl.DateTimeFormat("fr-CA", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    }).format(date);
  };
  const formatHasVulnerabilityStatus = (value: boolean): string =>
    value ? t("group.toe.ports.vulnerable") : t("group.toe.ports.safe");

  const storeUpdatedPort: (
    rootId: string,
    address: string,
    port: number,
    updatedToePort: IToePortAttr
  ) => void = (
    rootId: string,
    address: string,
    port: number,
    updatedToePort: IToePortAttr
  ): void => {
    client.writeQuery({
      data: {
        ...data,
        group: {
          ...data?.group,
          toePorts: {
            ...data?.group.toePorts,
            edges: data?.group.toePorts.edges.map(
              (value: IToePortEdge): IToePortEdge =>
                value.node.address === address &&
                value.node.port === port &&
                isEqualRootId(value.node.root, rootId)
                  ? {
                      node: updatedToePort,
                    }
                  : {
                      node: value.node,
                    }
            ),
          },
        },
      },
      query: GET_TOE_PORTS,
      variables: {
        ...getToePortsVariables,
        first: 150,
      },
    });
  };

  const handleUpdateToePortBePresent: (
    rootId: string,
    address: string,
    port: number,
    bePresent: boolean
  ) => Promise<void> = async (
    rootId: string,
    address: string,
    port: number,
    bePresent: boolean
  ): Promise<void> => {
    const result = await handleUpdateToePort({
      variables: {
        ...getToePortsVariables,
        address,
        bePresent,
        groupName,
        hasRecentAttack: undefined,
        port,
        rootId,
        shouldGetNewToePort: true,
      },
    });

    if (!_.isNil(result.data) && result.data.updateToePort.success) {
      const updatedToePort = result.data.updateToePort.toePort;
      if (!_.isUndefined(updatedToePort)) {
        setSelectedToePortDatas(
          selectedToePortDatas
            .map(
              (toePortData: IToePortData): IToePortData =>
                toePortData.address === address &&
                toePortData.port === port &&
                toePortData.rootId === rootId
                  ? formatToePortData(updatedToePort)
                  : toePortData
            )
            .filter(
              (toePortData: IToePortData): boolean => toePortData.bePresent
            )
        );
        storeUpdatedPort(rootId, address, port, updatedToePort);
      }
      msgSuccess(
        t("group.toe.ports.alerts.updatePort"),
        t("groupAlerts.updatedTitle")
      );
    }
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
      accessorFn: (row: IToePortData): string =>
        formatHasVulnerabilityStatus(row.hasVulnerabilities),
      cell: (cell: ICellHelper<IToePortData>): JSX.Element =>
        statusFormatter(cell.getValue()),
      header: String(t("group.toe.ports.status")),
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
      cell: (cell: ICellHelper<IToePortData>): JSX.Element | string =>
        editableBePresentFormatter(
          cell.row.original,
          canUpdateToePort && isInternal,
          handleUpdateToePortBePresent
        ),
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
      label: t("group.toe.ports.status"),
      selectOptions: [
        { header: formatHasVulnerabilityStatus(true), value: "true" },
        { header: formatHasVulnerabilityStatus(false), value: "false" },
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

  const toggleAdd = useCallback((): void => {
    setIsAdding(!isAdding);
  }, [isAdding]);

  const handleOnMarkAsAttackedCompleted = useCallback(
    (result: FetchResult<IUpdateToePortResultAttr>): void => {
      if (!_.isNil(result.data) && result.data.updateToePort.success) {
        msgSuccess(
          t("group.toe.ports.alerts.markAsAttacked.success"),
          t("groupAlerts.updatedTitle")
        );
        void refetch();
        setSelectedToePortDatas([]);
      }
    },
    [refetch, t]
  );

  const handleMarkAsAttacked = useCallback(async (): Promise<void> => {
    const presentSelectedToePortDatas = selectedToePortDatas.filter(
      (toePortData: IToePortData): boolean => toePortData.bePresent
    );
    setIsMarkingAsAttacked(true);
    const results = await Promise.all(
      presentSelectedToePortDatas.map(
        async (
          toePortData: IToePortData
        ): Promise<FetchResult<IUpdateToePortResultAttr>> =>
          handleUpdateToePort({
            variables: {
              ...getToePortsVariables,
              address: toePortData.address,
              bePresent: toePortData.bePresent,
              groupName,
              hasRecentAttack: true,
              port: toePortData.port,
              rootId: toePortData.rootId,
              shouldGetNewToePort: false,
            },
          })
      )
    );
    const errors = getErrors<IUpdateToePortResultAttr>(results);

    if (!_.isEmpty(results) && _.isEmpty(errors)) {
      handleOnMarkAsAttackedCompleted(results[0]);
    } else {
      void refetch();
    }
    setIsMarkingAsAttacked(false);
  }, [
    getToePortsVariables,
    groupName,
    handleOnMarkAsAttackedCompleted,
    handleUpdateToePort,
    refetch,
    selectedToePortDatas,
  ]);

  const enabledRows = useCallback((row: Row<IToePortData>): boolean => {
    return row.original.bePresent;
  }, []);

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
        extraButtons={
          <ActionButtons
            arePortsSelected={selectedToePortDatas.length > 0}
            isAdding={isAdding}
            isInternal={isInternal}
            isMarkingAsAttacked={isMarkingAsAttacked}
            onAdd={toggleAdd}
            onMarkAsAttacked={handleMarkAsAttacked}
          />
        }
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
      {isAdding ? (
        <HandleAdditionModal
          groupName={groupName}
          handleCloseModal={toggleAdd}
          refetchData={refetch}
        />
      ) : undefined}
    </React.StrictMode>
  );
};

export { GroupToePortsView };
