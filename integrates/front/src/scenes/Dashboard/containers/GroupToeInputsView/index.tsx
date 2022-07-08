import { useApolloClient, useMutation, useQuery } from "@apollo/client";
import type { ApolloError, FetchResult } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import moment from "moment";
import type { ChangeEvent } from "react";
import React, { useCallback, useEffect, useState } from "react";
import type { SortOrder } from "react-bootstrap-table-next";
import { dateFilter } from "react-bootstrap-table2-filter";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { ActionButtons } from "./ActionButtons";
import { editableBePresentFormatter } from "./formatters/editableBePresentFormatter";
import { HandleAdditionModal } from "./HandleAdditionModal";
import {
  formatBePresent,
  formatRootId,
  getFilteredData,
  getNonSelectableToeInputIndex,
  getToeInputIndex,
  onSelectSeveralToeInputHelper,
} from "./utils";

import { Table } from "components/Table";
import type {
  IFilterProps,
  IHeaderConfig,
  ISelectRowProps,
} from "components/Table/types";
import {
  GET_TOE_INPUTS,
  UPDATE_TOE_INPUT,
} from "scenes/Dashboard/containers/GroupToeInputsView/queries";
import type {
  IFilterSet,
  IGroupToeInputsViewProps,
  IToeInputAttr,
  IToeInputData,
  IToeInputEdge,
  IToeInputsConnection,
  IUpdateToeInputResultAttr,
} from "scenes/Dashboard/containers/GroupToeInputsView/types";
import { GET_ROOT_IDS } from "scenes/Dashboard/queries";
import type { IGroupRootIdsAttr, IRootIdAttr } from "scenes/Dashboard/types";
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
  const [searchTextFilter, setSearchTextFilter] = useState("");
  const [selectedToeInputDatas, setSelectedToeInputDatas] = useState<
    IToeInputData[]
  >([]);

  const [checkedItems, setCheckedItems] = useStoredState<
    Record<string, boolean>
  >(
    "toeInputsTableSet",
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
  const [filterGroupToeInputTable, setFilterGroupToeInputTable] =
    useStoredState<IFilterSet>(
      `filterGroupToeInputSet-${groupName}`,
      {
        bePresent: "",
        component: "",
        hasVulnerabilities: "",
        rootId: "",
        seenAt: { max: "", min: "" },
        seenFirstTimeBy: "",
      },
      localStorage
    );
  const [isCustomFilterEnabled, setCustomFilterEnabled] =
    useStoredState<boolean>("toeInputCustomFilters", false);
  const handleChange: (columnName: string) => void = useCallback(
    (columnName: string): void => {
      if (
        Object.values(checkedItems).filter((val: boolean): boolean => val)
          .length === 1 &&
        checkedItems[columnName]
      ) {
        // eslint-disable-next-line no-alert
        alert(t("validations.columns"));
        setCheckedItems({
          ...checkedItems,
          [columnName]: true,
        });
      } else {
        setCheckedItems({
          ...checkedItems,
          [columnName]: !checkedItems[columnName],
        });
      }
    },
    [checkedItems, setCheckedItems, t]
  );
  const handleUpdateCustomFilter: () => void = useCallback((): void => {
    setCustomFilterEnabled(!isCustomFilterEnabled);
  }, [isCustomFilterEnabled, setCustomFilterEnabled]);

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
    rootId: formatRootId(filterGroupToeInputTable.rootId),
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
      bePresent: formatBePresent(filterGroupToeInputTable.bePresent),
      first: 150,
    },
  });
  const { data: rootIdsData } = useQuery<IGroupRootIdsAttr>(GET_ROOT_IDS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load group root ids", error);
      });
    },
    variables: {
      groupName,
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

  const onSort: (dataField: string, order: SortOrder) => void = (
    dataField: string,
    order: SortOrder
  ): void => {
    const newSorted = { dataField, order };
    sessionStorage.setItem("toeInputsSort", JSON.stringify(newSorted));
  };

  const formatCsvEntrypoint = (value: string): string =>
    `'${value.trim().replace('"', '""')}`;

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
            bePresent: formatBePresent(filterGroupToeInputTable.bePresent),
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

  const headersToeInputsTable: IHeaderConfig[] = [
    {
      dataField: "rootNickname",
      header: t("group.toe.inputs.root"),
      onSort,
      visible: checkedItems.rootNickname,
    },
    {
      dataField: "component",
      header: t("group.toe.inputs.component"),
      onSort,
      visible: checkedItems.component,
    },
    {
      csvFormatter: formatCsvEntrypoint,
      dataField: "entryPoint",
      header: t("group.toe.inputs.entryPoint"),
      onSort,
      visible: checkedItems.entryPoint,
    },
    {
      dataField: "hasVulnerabilities",
      formatter: formatBoolean,
      header: t("group.toe.inputs.hasVulnerabilities"),
      onSort,
      visible: checkedItems.hasVulnerabilities,
    },
    {
      dataField: "attackedAt",
      filter: dateFilter({}),
      formatter: formatDate,
      header: t("group.toe.inputs.attackedAt"),
      omit: !isInternal || !canGetAttackedAt,
      onSort,
      visible: checkedItems.attackedAt,
    },
    {
      dataField: "attackedBy",
      header: t("group.toe.inputs.attackedBy"),
      omit: !isInternal || !canGetAttackedBy,
      onSort,
      visible: checkedItems.attackedBy,
    },
    {
      dataField: "firstAttackAt",
      filter: dateFilter({}),
      formatter: formatDate,
      header: t("group.toe.inputs.firstAttackAt"),
      omit: !isInternal || !canGetFirstAttackAt,
      onSort,
      visible: checkedItems.firstAttackAt,
    },
    {
      dataField: "seenAt",
      filter: dateFilter({}),
      formatter: formatDate,
      header: t("group.toe.inputs.seenAt"),
      onSort,
      visible: checkedItems.seenAt,
    },
    {
      dataField: "seenFirstTimeBy",
      header: t("group.toe.inputs.seenFirstTimeBy"),
      omit: !isInternal || !canGetSeenFirstTimeBy,
      onSort,
      visible: checkedItems.seenFirstTimeBy,
    },
    {
      dataField: "bePresent",
      formatter: editableBePresentFormatter(
        canUpdateToeInput && isInternal,
        handleUpdateToeInputBePresent
      ),
      header: t("group.toe.inputs.bePresent"),
      onSort,
      visible: checkedItems.bePresent,
    },
    {
      dataField: "bePresentUntil",
      filter: dateFilter({}),
      formatter: formatDate,
      header: t("group.toe.inputs.bePresentUntil"),
      omit: !isInternal || !canGetBePresentUntil,
      onSort,
      visible: checkedItems.bePresentUntil,
    },
  ];

  const roots = rootIdsData === undefined ? [] : rootIdsData.group.roots;
  function clearFilters(): void {
    setFilterGroupToeInputTable(
      (): IFilterSet => ({
        bePresent: "",
        component: "",
        hasVulnerabilities: "",
        rootId: "",
        seenAt: { max: "", min: "" },
        seenFirstTimeBy: "",
      })
    );
    setSearchTextFilter("");
  }
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
  }, [
    filterGroupToeInputTable.bePresent,
    filterGroupToeInputTable.rootId,
    refetch,
  ]);

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

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

  const onBasicFilterValueChange = (
    filterName: keyof IFilterSet
  ): ((event: ChangeEvent<HTMLSelectElement>) => void) => {
    return (event: React.ChangeEvent<HTMLSelectElement>): void => {
      event.persist();
      setFilterGroupToeInputTable(
        (value): IFilterSet => ({
          ...value,
          [filterName]: event.target.value,
        })
      );
    };
  };
  const onRangeFilterValueChange = (
    filterName: keyof Pick<IFilterSet, "seenAt">,
    key: "max" | "min"
  ): ((event: ChangeEvent<HTMLInputElement>) => void) => {
    return (event: React.ChangeEvent<HTMLInputElement>): void => {
      event.persist();

      setFilterGroupToeInputTable(
        (value): IFilterSet => ({
          ...value,
          [filterName]: { ...value[filterName], [key]: event.target.value },
        })
      );
    };
  };
  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }
  const componentSelectOptions = Object.fromEntries(
    toeInputs.map((toeInputData: IToeInputData): string[] => [
      toeInputData.component,
      toeInputData.component,
    ])
  );
  const rootSelectOptions = Object.fromEntries(
    roots.map((root: IRootIdAttr): string[] => [
      root.id,
      `${root.nickname} (${root.state.toLowerCase()})`,
    ])
  );
  const booleanSelectOptions = Object.fromEntries([
    ["false", formatBoolean(false)],
    ["true", formatBoolean(true)],
  ]);
  const seenFirstTimeBySelectOptions = Object.fromEntries(
    toeInputs.map((toeInputData: IToeInputData): string[] => [
      toeInputData.markedSeenFirstTimeBy,
      toeInputData.seenFirstTimeBy,
    ])
  );
  const customFiltersProps: IFilterProps[] = [
    {
      defaultValue: filterGroupToeInputTable.rootId,
      onChangeSelect: onBasicFilterValueChange("rootId"),
      placeholder: t("group.toe.inputs.filters.root.placeholder"),
      selectOptions: rootSelectOptions,
      tooltipId: "group.toe.inputs.filters.root.tooltip.id",
      tooltipMessage: "group.toe.inputs.filters.root.tooltip",
      type: "select",
    },
    {
      defaultValue: filterGroupToeInputTable.component,
      onChangeSelect: onBasicFilterValueChange("component"),
      placeholder: t("group.toe.inputs.filters.component.placeholder"),
      selectOptions: componentSelectOptions,
      tooltipId: "group.toe.inputs.filters.component.tooltip.id",
      tooltipMessage: "group.toe.inputs.filters.component.tooltip",
      translateSelectOptions: false,
      type: "select",
    },
    {
      defaultValue: filterGroupToeInputTable.hasVulnerabilities,
      onChangeSelect: onBasicFilterValueChange("hasVulnerabilities"),
      placeholder: t("group.toe.inputs.filters.hasVulnerabilities.placeholder"),
      selectOptions: booleanSelectOptions,
      tooltipId: "group.toe.inputs.filters.hasVulnerabilities.tooltip.id",
      tooltipMessage: "group.toe.inputs.filters.hasVulnerabilities.tooltip",
      type: "select",
    },
    {
      defaultValue: "",
      placeholder: t("group.toe.inputs.filters.seenAt.placeholder"),
      rangeProps: {
        defaultValue: filterGroupToeInputTable.seenAt,
        onChangeMax: onRangeFilterValueChange("seenAt", "max"),
        onChangeMin: onRangeFilterValueChange("seenAt", "min"),
      },
      tooltipId: "group.toe.inputs.filters.seenAt.tooltip.id",
      tooltipMessage: "group.toe.inputs.filters.seenAt.tooltip",
      type: "dateRange",
    },
    {
      defaultValue: filterGroupToeInputTable.seenFirstTimeBy,
      omit: !isInternal || !canGetSeenFirstTimeBy,
      onChangeSelect: onBasicFilterValueChange("seenFirstTimeBy"),
      placeholder: t("group.toe.inputs.filters.seenFirstTimeBy.placeholder"),
      selectOptions: seenFirstTimeBySelectOptions,
      tooltipId: "group.toe.inputs.filters.seenFirstTimeBy.tooltip.id",
      tooltipMessage: "group.toe.inputs.filters.seenFirstTimeBy.tooltip",
      type: "select",
    },
    {
      defaultValue: filterGroupToeInputTable.bePresent,
      onChangeSelect: onBasicFilterValueChange("bePresent"),
      placeholder: t("group.toe.inputs.filters.bePresent.placeholder"),
      selectOptions: booleanSelectOptions,
      tooltipId: "group.toe.inputs.filters.bePresent.tooltip.id",
      tooltipMessage: "group.toe.inputs.filters.bePresent.tooltip",
      type: "select",
    },
  ];
  const filteredData: IToeInputData[] = getFilteredData(
    filterGroupToeInputTable,
    searchTextFilter,
    toeInputs
  );

  function onSelectSeveralToeInputDatas(
    isSelect: boolean,
    toeInputDatasSelected: IToeInputData[]
  ): string[] {
    return onSelectSeveralToeInputHelper(
      isSelect,
      toeInputDatasSelected,
      selectedToeInputDatas,
      setSelectedToeInputDatas
    );
  }
  function onSelectOneToeInputData(
    toeInputdata: IToeInputData,
    isSelect: boolean
  ): boolean {
    onSelectSeveralToeInputDatas(isSelect, [toeInputdata]);

    return true;
  }
  const selectionMode: ISelectRowProps = {
    clickToSelect: false,
    hideSelectColumn: !isInternal || !canUpdateToeInput,
    mode: "checkbox",
    nonSelectable: getNonSelectableToeInputIndex(filteredData),
    onSelect: onSelectOneToeInputData,
    onSelectAll: onSelectSeveralToeInputDatas,
    selected: getToeInputIndex(selectedToeInputDatas, filteredData),
  };

  const initialSort: string = JSON.stringify({
    dataField: "component",
    order: "asc",
  });

  return (
    <React.StrictMode>
      <Table
        clearFiltersButton={clearFilters}
        columnToggle={true}
        customFilters={{
          customFiltersProps,
          isCustomFilterEnabled,
          onUpdateEnableCustomFilter: handleUpdateCustomFilter,
        }}
        customSearch={{
          customSearchDefault: searchTextFilter,
          isCustomSearchEnabled: true,
          onUpdateCustomSearch: onSearchTextChange,
          position: "right",
        }}
        dataset={filteredData}
        defaultSorted={JSON.parse(
          _.get(sessionStorage, "toeInputsSort", initialSort) as string
        )}
        exportCsv={true}
        extraButtonsRight={
          <ActionButtons
            areInputsSelected={selectedToeInputDatas.length > 0}
            isAdding={isAdding}
            isInternal={isInternal}
            isMarkingAsAttacked={isMarkingAsAttacked}
            onAdd={toggleAdd}
            onMarkAsAttacked={handleMarkAsAttacked}
          />
        }
        headers={headersToeInputsTable}
        id={"tblToeInputs"}
        isFilterEnabled={undefined}
        onColumnToggle={handleChange}
        pageSize={100}
        search={false}
        selectionMode={selectionMode}
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
