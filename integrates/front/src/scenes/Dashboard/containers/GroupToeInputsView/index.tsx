/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useApolloClient, useMutation, useQuery } from "@apollo/client";
import type { ApolloError, FetchResult } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type {
  ColumnDef,
  ColumnFiltersState,
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

import { ActionButtons } from "./ActionButtons";
import { editableBePresentFormatter } from "./formatters/editableBePresentFormatter";
import { HandleAdditionModal } from "./HandleAdditionModal";
import { getNonSelectableToeInputIndex } from "./utils";

import { Table } from "components/Table";
import { filterDate } from "components/Table/filters/filterFunctions/filterDate";
import type { ICellHelper } from "components/Table/types";
import {
  GET_TOE_INPUTS,
  UPDATE_TOE_INPUT,
} from "scenes/Dashboard/containers/GroupToeInputsView/queries";
import type {
  IGroupToeInputsViewProps,
  IToeInputAttr,
  IToeInputData,
  IToeInputEdge,
  IToeInputsConnection,
  IUpdateToeInputResultAttr,
} from "scenes/Dashboard/containers/GroupToeInputsView/types";
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

  const [columnFilters, setColumnFilters] = useStoredState<ColumnFiltersState>(
    "tblToeInputs-columnFilters",
    [],
    localStorage
  );
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

    return moment(date).format("YYYY-MM-DD");
  };

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
        return formatBoolean(row.hasVulnerabilities);
      },
      header: String(t("group.toe.inputs.hasVulnerabilities")),
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
      header: String(t("group.toe.inputs.bePresent")),
      id: "bePresent",
      meta: { filterType: "select" },
    },
  ];

  const columnsAttackedAt: ColumnDef<IToeInputData>[] =
    isInternal && canGetAttackedAt
      ? [
          {
            accessorKey: "attackedAt",
            cell: (cell: ICellHelper<IToeInputData>): string =>
              formatDate(cell.getValue()),
            filterFn: filterDate,
            header: t("group.toe.inputs.attackedAt"),
            meta: { filterType: "dateRange" },
          },
        ]
      : [];

  const columnsAttackedBy: ColumnDef<IToeInputData>[] =
    isInternal && canGetAttackedBy
      ? [
          {
            accessorKey: "attackedBy",
            header: t("group.toe.inputs.attackedBy"),
          },
        ]
      : [];
  const columnsFirstAttackAt: ColumnDef<IToeInputData>[] =
    isInternal && canGetFirstAttackAt
      ? [
          {
            accessorKey: "firstAttackAt",
            cell: (cell: ICellHelper<IToeInputData>): string =>
              formatDate(cell.getValue()),
            filterFn: filterDate,
            header: t("group.toe.inputs.firstAttackAt"),
            meta: { filterType: "dateRange" },
          },
        ]
      : [];
  const columnsSeenFirstTimeBy: ColumnDef<IToeInputData>[] =
    isInternal && canGetSeenFirstTimeBy
      ? [
          {
            accessorKey: "seenFirstTimeBy",
            header: t("group.toe.inputs.seenFirstTimeBy"),
          },
        ]
      : [];
  const columnsbePresentUntil: ColumnDef<IToeInputData>[] =
    isInternal && canGetBePresentUntil
      ? [
          {
            accessorKey: "bePresentUntil",
            cell: (cell: ICellHelper<IToeInputData>): string =>
              formatDate(cell.getValue()),
            filterFn: filterDate,
            header: t("group.toe.inputs.bePresentUntil"),
            meta: { filterType: "dateRange" },
          },
        ]
      : [];

  const columnsResult: ColumnDef<IToeInputData>[] = columns
    .concat(columnsAttackedAt)
    .concat(columnsAttackedBy)
    .concat(columnsFirstAttackAt)
    .concat(columnsSeenFirstTimeBy)
    .concat(columnsbePresentUntil);

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

  function toggleAdd(): void {
    setIsAdding(!isAdding);
  }

  const handleOnMarkAsAttackedCompleted = (
    result: FetchResult<IUpdateToeInputResultAttr>
  ): void => {
    if (!_.isNil(result.data) && result.data.updateToeInput.success) {
      msgSuccess(
        t("group.toe.inputs.alerts.markAsAttacked.success"),
        t("groupAlerts.updatedTitle")
      );
      void refetch();
      setSelectedToeInputDatas([]);
    }
  };

  async function handleMarkAsAttacked(): Promise<void> {
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
  }

  function enabledRows(row: Row<IToeInputData>): boolean {
    const indexes = getNonSelectableToeInputIndex(toeInputs);
    const nonselectables = indexes.map(
      (index: number): IToeInputData => toeInputs[index]
    );

    return !nonselectables.includes(row.original);
  }

  return (
    <React.StrictMode>
      <Table
        columnFilterSetter={setColumnFilters}
        columnFilterState={columnFilters}
        columnToggle={true}
        columnVisibilitySetter={setColumnVisibility}
        columnVisibilityState={columnVisibility}
        columns={columnsResult}
        data={toeInputs}
        enableColumnFilters={true}
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
