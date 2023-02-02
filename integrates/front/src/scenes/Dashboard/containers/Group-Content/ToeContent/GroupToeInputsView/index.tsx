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

import type { IFilter } from "components/Filter";
import { Filters, useFilters } from "components/Filter";
import { Table } from "components/Table";
import { filterDate } from "components/Table/filters/filterFunctions/filterDate";
import type { ICellHelper } from "components/Table/types";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter";
import {
  GET_TOE_INPUTS,
  UPDATE_TOE_INPUT,
} from "scenes/Dashboard/containers/Group-Content/ToeContent/GroupToeInputsView/queries";
import type {
  IGroupToeInputsViewProps,
  IToeInputAttr,
  IToeInputData,
  IToeInputEdge,
  IToeInputsConnection,
  IUpdateToeInputResultAttr,
} from "scenes/Dashboard/containers/Group-Content/ToeContent/GroupToeInputsView/types";
import { authzPermissionsContext } from "utils/authz/config";
import { getErrors } from "utils/helpers";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const NOSEENFIRSTTIMEBY = "no seen first time by";

const GroupToeInputsView: React.FC<IGroupToeInputsViewProps> = ({
  isInternal,
}: IGroupToeInputsViewProps): JSX.Element => {
  const { t } = useTranslation();
  const client = useApolloClient();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canGetAttackedAt: boolean = permissions.can(
    "api_resolvers_toe_input_attacked_at_resolve"
  );
  const canGetAttackedBy: boolean = permissions.can(
    "api_resolvers_toe_input_attacked_by_resolve"
  );
  const canGetBePresentUntil: boolean = permissions.can(
    "api_resolvers_toe_input_be_present_until_resolve"
  );
  const canGetFirstAttackAt: boolean = permissions.can(
    "api_resolvers_toe_input_first_attack_at_resolve"
  );
  const canGetSeenFirstTimeBy: boolean = permissions.can(
    "api_resolvers_toe_input_seen_first_time_by_resolve"
  );
  const canUpdateToeInput: boolean = permissions.can(
    "api_mutations_update_toe_input_mutate"
  );

  const { groupName } = useParams<{ groupName: string }>();
  const [isAdding, setIsAdding] = useState(false);
  const [isMarkingAsAttacked, setIsMarkingAsAttacked] = useState(false);
  const [selectedToeInputDatas, setSelectedToeInputDatas] = useState<
    IToeInputData[]
  >([]);

  const [columnVisibility, setColumnVisibility] =
    useStoredState<VisibilityState>(
      "tblToeInputs-visibilityState",
      {
        attackedAt: true,
        attackedBy: false,
        bePresent: false,
        bePresentUntil: false,
        component: false,
        entryPoint: true,
        firstAttackAt: false,
        hasVulnerabilities: true,
        rootNickname: true,
        seenAt: true,
        seenFirstTimeBy: true,
      },
      localStorage
    );
  const [sorting, setSorting] = useStoredState<SortingState>(
    "tblToeInputs-sortingState",
    []
  );

  // // GraphQL operations
  const [handleUpdateToeInput] = useMutation<IUpdateToeInputResultAttr>(
    UPDATE_TOE_INPUT,
    {
      onError: (errors: ApolloError): void => {
        errors.graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - The toe input is not present":
              msgError(t("group.toe.inputs.alerts.nonPresent"));
              break;
            case "Exception - The attack time must be between the previous attack and the current time":
              msgError(t("group.toe.inputs.alerts.invalidAttackedAt"));
              break;
            case "Exception - The toe input has been updated by another operation":
              msgError(t("group.toe.inputs.alerts.alreadyUpdate"));
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning("An error occurred updating the toe input", error);
          }
        });
      },
    }
  );

  // eslint-disable-next-line react-hooks/exhaustive-deps
  const getToeInputsVariables = {
    canGetAttackedAt,
    canGetAttackedBy,
    canGetBePresentUntil,
    canGetFirstAttackAt,
    canGetSeenFirstTimeBy,
    groupName,
  };
  const { data, fetchMore, refetch } = useQuery<{
    group: { toeInputs: IToeInputsConnection };
  }>(GET_TOE_INPUTS, {
    fetchPolicy: "network-only",
    nextFetchPolicy: "cache-first",
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load toe inputs", error);
      });
    },
    variables: {
      ...getToeInputsVariables,
      first: 150,
    },
  });
  const pageInfo =
    data === undefined ? undefined : data.group.toeInputs.pageInfo;
  const toeInputsEdges: IToeInputEdge[] =
    data === undefined ? [] : data.group.toeInputs.edges;
  const formatOptionalDate: (date: string | null) => Date | undefined = (
    date: string | null
  ): Date | undefined => (_.isNull(date) ? undefined : new Date(date));
  const markSeenFirstTimeBy: (seenFirstTimeBy: string) => string = (
    seenFirstTimeBy: string
  ): string =>
    _.isEmpty(seenFirstTimeBy) ? NOSEENFIRSTTIMEBY : seenFirstTimeBy;
  const formatToeInputData: (toeInputAttr: IToeInputAttr) => IToeInputData = (
    toeInputAttr: IToeInputAttr
  ): IToeInputData => ({
    ...toeInputAttr,
    attackedAt: formatOptionalDate(toeInputAttr.attackedAt),
    bePresentUntil: formatOptionalDate(toeInputAttr.bePresentUntil),
    firstAttackAt: formatOptionalDate(toeInputAttr.firstAttackAt),
    markedSeenFirstTimeBy: markSeenFirstTimeBy(toeInputAttr.seenFirstTimeBy),
    rootId: _.isNil(toeInputAttr.root) ? "" : toeInputAttr.root.id,
    rootNickname: _.isNil(toeInputAttr.root) ? "" : toeInputAttr.root.nickname,
    seenAt: formatOptionalDate(toeInputAttr.seenAt),
  });
  const toeInputs: IToeInputData[] = toeInputsEdges.map(
    ({ node }): IToeInputData => formatToeInputData(node)
  );

  const formatBoolean = (value: boolean): string =>
    value ? t("group.toe.inputs.yes") : t("group.toe.inputs.no");
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
    value ? t("group.toe.inputs.vulnerable") : t("group.toe.inputs.safe");

  const handleUpdateToeInputBePresent: (
    rootId: string,
    component: string,
    entryPoint: string,
    bePresent: boolean
  ) => Promise<void> = async (
    rootId: string,
    component: string,
    entryPoint: string,
    bePresent: boolean
  ): Promise<void> => {
    const result = await handleUpdateToeInput({
      variables: {
        ...getToeInputsVariables,
        bePresent,
        component,
        entryPoint,
        groupName,
        hasRecentAttack: undefined,
        rootId,
        shouldGetNewToeInput: true,
      },
    });

    if (!_.isNil(result.data) && result.data.updateToeInput.success) {
      const updatedToeInput = result.data.updateToeInput.toeInput;
      if (!_.isUndefined(updatedToeInput)) {
        setSelectedToeInputDatas(
          selectedToeInputDatas
            .map(
              (toeInputData: IToeInputData): IToeInputData =>
                toeInputData.component === component &&
                toeInputData.entryPoint === entryPoint &&
                toeInputData.rootId === rootId
                  ? formatToeInputData(updatedToeInput)
                  : toeInputData
            )
            .filter(
              (toeInputData: IToeInputData): boolean => toeInputData.bePresent
            )
        );
        client.writeQuery({
          data: {
            ...data,
            group: {
              ...data?.group,
              toeInputs: {
                ...data?.group.toeInputs,
                edges: data?.group.toeInputs.edges.map(
                  (value: IToeInputEdge): IToeInputEdge =>
                    value.node.component === component &&
                    value.node.entryPoint === entryPoint &&
                    (_.isNil(value.node.root) ? "" : value.node.root.id) ===
                      rootId
                      ? {
                          node: updatedToeInput,
                        }
                      : {
                          node: value.node,
                        }
                ),
              },
            },
          },
          query: GET_TOE_INPUTS,
          variables: {
            ...getToeInputsVariables,
            first: 150,
          },
        });
      }
      msgSuccess(
        t("group.toe.inputs.alerts.updateInput"),
        t("groupAlerts.updatedTitle")
      );
    }
  };

  const columns: ColumnDef<IToeInputData>[] = [
    {
      accessorKey: "rootNickname",
      header: t("group.toe.inputs.root"),
      meta: { filterType: "select" },
    },
    {
      accessorKey: "component",
      header: t("group.toe.inputs.component"),
      meta: { filterType: "select" },
    },
    {
      accessorKey: "entryPoint",
      header: t("group.toe.inputs.entryPoint"),
    },
    {
      accessorFn: (row: IToeInputData): string => {
        return formatHasVulnerabilityStatus(row.hasVulnerabilities);
      },
      cell: (cell: ICellHelper<IToeInputData>): JSX.Element =>
        statusFormatter(cell.getValue()),
      header: String(t("group.toe.inputs.status")),
      meta: { filterType: "select" },
    },
    {
      accessorKey: "seenAt",
      cell: (cell: ICellHelper<IToeInputData>): string =>
        formatDate(cell.getValue()),
      filterFn: filterDate,
      header: t("group.toe.inputs.seenAt"),
      meta: { filterType: "dateRange" },
    },
    {
      accessorFn: (row: IToeInputData): string => {
        return formatBoolean(row.bePresent);
      },
      cell: (cell: ICellHelper<IToeInputData>): JSX.Element | string =>
        editableBePresentFormatter(
          cell.row.original,
          canUpdateToeInput && isInternal,
          handleUpdateToeInputBePresent
        ),
      header: t("group.toe.inputs.bePresent"),
      id: "bePresent",
      meta: { filterType: "select" },
    },
    {
      accessorKey: "attackedAt",
      cell: (cell: ICellHelper<IToeInputData>): string =>
        formatDate(cell.getValue()),
      filterFn: filterDate,
      header: t("group.toe.inputs.attackedAt"),
      id: "attackedAt",
      meta: { filterType: "dateRange" },
    },
    {
      accessorKey: "attackedBy",
      header: t("group.toe.inputs.attackedBy"),
      id: "attackedBy",
    },
    {
      accessorKey: "firstAttackAt",
      cell: (cell: ICellHelper<IToeInputData>): string =>
        formatDate(cell.getValue()),
      filterFn: filterDate,
      header: t("group.toe.inputs.firstAttackAt"),
      id: "firstAttackAt",
      meta: { filterType: "dateRange" },
    },
    {
      accessorKey: "seenFirstTimeBy",
      header: t("group.toe.inputs.seenFirstTimeBy"),
      id: "seenFirstTimeBy",
    },
    {
      accessorKey: "bePresentUntil",
      cell: (cell: ICellHelper<IToeInputData>): string =>
        formatDate(cell.getValue()),
      filterFn: filterDate,
      header: t("group.toe.inputs.bePresentUntil"),
      id: "bePresentUntil",
      meta: { filterType: "dateRange" },
    },
  ];

  const baseFilters: IFilter<IToeInputData>[] = [
    {
      id: "rootNickname",
      key: "rootNickname",
      label: t("group.toe.inputs.root"),
      selectOptions: (inputs): string[] =>
        [
          ...new Set(inputs.map((datapoint): string => datapoint.rootNickname)),
        ].filter(Boolean),
      type: "select",
    },
    {
      id: "component",
      key: "component",
      label: t("group.toe.inputs.component"),
      selectOptions: (inputs): string[] =>
        [
          ...new Set(inputs.map((datapoint): string => datapoint.component)),
        ].filter(Boolean),
      type: "select",
    },
    {
      id: "entryPoint",
      key: "entryPoint",
      label: t("group.toe.inputs.entryPoint"),
      type: "text",
    },
    {
      id: "hasVulnerabilities",
      key: "hasVulnerabilities",
      label: t("group.toe.inputs.status"),
      selectOptions: [
        { header: formatHasVulnerabilityStatus(true), value: "true" },
        { header: formatHasVulnerabilityStatus(false), value: "false" },
      ],
      type: "select",
    },
    {
      id: "seenAt",
      key: "seenAt",
      label: t("group.toe.inputs.seenAt"),
      type: "dateRange",
    },
    {
      id: "bePresent",
      key: "bePresent",
      label: t("group.toe.inputs.bePresent"),
      selectOptions: [
        { header: formatBoolean(true), value: "true" },
        { header: formatBoolean(false), value: "false" },
      ],
      type: "select",
    },
    {
      id: "attackedAt",
      key: "attackedAt",
      label: t("group.toe.inputs.attackedAt"),
      type: "dateRange",
    },
    {
      id: "attackedBy",
      key: "attackedBy",
      label: t("group.toe.inputs.attackedBy"),
      type: "text",
    },
    {
      id: "firstAttackAt",
      key: "firstAttackAt",
      label: t("group.toe.inputs.firstAttackAt"),
      type: "dateRange",
    },
    {
      id: "seenFirstTimeBy",
      key: "seenFirstTimeBy",
      label: t("group.toe.inputs.seenFirstTimeBy"),
      type: "text",
    },
    {
      id: "bePresentUntil",
      key: "bePresentUntil",
      label: t("group.toe.inputs.bePresentUntil"),
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

  const [filters, setFilters] =
    useState<IFilter<IToeInputData>[]>(tableFilters);

  const filteredToeLines = useFilters(toeInputs, filters);

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
    setSelectedToeInputDatas([]);
    void refetch();
  }, [refetch]);

  const toggleAdd = useCallback((): void => {
    setIsAdding(!isAdding);
  }, [isAdding]);

  const handleOnMarkAsAttackedCompleted = useCallback(
    (result: FetchResult<IUpdateToeInputResultAttr>): void => {
      if (!_.isNil(result.data) && result.data.updateToeInput.success) {
        msgSuccess(
          t("group.toe.inputs.alerts.markAsAttacked.success"),
          t("groupAlerts.updatedTitle")
        );
        void refetch();
        setSelectedToeInputDatas([]);
      }
    },
    [refetch, t]
  );

  const handleMarkAsAttacked = useCallback(async (): Promise<void> => {
    const presentSelectedToeInputDatas = selectedToeInputDatas.filter(
      (toeInputData: IToeInputData): boolean => toeInputData.bePresent
    );
    setIsMarkingAsAttacked(true);
    const results = await Promise.all(
      presentSelectedToeInputDatas.map(
        async (
          toeInputData: IToeInputData
        ): Promise<FetchResult<IUpdateToeInputResultAttr>> =>
          handleUpdateToeInput({
            variables: {
              ...getToeInputsVariables,
              bePresent: toeInputData.bePresent,
              component: toeInputData.component,
              entryPoint: toeInputData.entryPoint,
              groupName,
              hasRecentAttack: true,
              rootId: toeInputData.rootId,
              shouldGetNewToeInput: false,
            },
          })
      )
    );

    const errors = getErrors<IUpdateToeInputResultAttr>(results);

    if (!_.isEmpty(results) && _.isEmpty(errors)) {
      handleOnMarkAsAttackedCompleted(results[0]);
    } else {
      void refetch();
    }
    setIsMarkingAsAttacked(false);
  }, [
    getToeInputsVariables,
    groupName,
    handleOnMarkAsAttackedCompleted,
    handleUpdateToeInput,
    refetch,
    selectedToeInputDatas,
  ]);

  const enabledRows = useCallback((row: Row<IToeInputData>): boolean => {
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
            areInputsSelected={selectedToeInputDatas.length > 0}
            isAdding={isAdding}
            isInternal={isInternal}
            isMarkingAsAttacked={isMarkingAsAttacked}
            onAdd={toggleAdd}
            onMarkAsAttacked={handleMarkAsAttacked}
          />
        }
        filters={
          <Filters
            dataset={toeInputs}
            filters={filters}
            setFilters={setFilters}
          />
        }
        id={"tblToeInputs"}
        rowSelectionSetter={
          !isInternal || !canUpdateToeInput
            ? undefined
            : setSelectedToeInputDatas
        }
        rowSelectionState={selectedToeInputDatas}
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

export { GroupToeInputsView };
