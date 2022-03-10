import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import moment from "moment";
import type { ChangeEvent } from "react";
import React, { useCallback, useEffect, useState } from "react";
import type { SortOrder } from "react-bootstrap-table-next";
import { dateFilter } from "react-bootstrap-table2-filter";
import { useParams } from "react-router-dom";

import { ActionButtons } from "./ActionButtons";
import { HandleAdditionModal } from "./HandleAdditionModal";
import { HandleEditionModal } from "./HandleEditionModal";
import {
  formatBePresent,
  formatRootId,
  getFilteredData,
  getToeInputIndex,
  onSelectSeveralToeInputHelper,
} from "./utils";

import { Table } from "components/Table";
import type {
  IFilterProps,
  IHeaderConfig,
  ISelectRowProps,
} from "components/Table/types";
import { GET_TOE_INPUTS } from "scenes/Dashboard/containers/GroupToeInputsView/queries";
import type {
  IFilterSet,
  IGroupToeInputsViewProps,
  IToeInputData,
  IToeInputEdge,
  IToeInputsConnection,
} from "scenes/Dashboard/containers/GroupToeInputsView/types";
import { GET_ROOT_IDS } from "scenes/Dashboard/queries";
import type { IGroupRootIdsAttr, IRootIdAttr } from "scenes/Dashboard/types";
import { authzPermissionsContext } from "utils/authz/config";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { translate } from "utils/translations/translate";

const NOSEENFIRSTTIMEBY = "no seen first time by";

const GroupToeInputsView: React.FC<IGroupToeInputsViewProps> = (
  props: IGroupToeInputsViewProps
): JSX.Element => {
  const { isInternal } = props;

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
  const [isEditing, setIsEditing] = useState(false);
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
        alert(translate.t("validations.columns"));
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
    [checkedItems, setCheckedItems]
  );
  const handleUpdateCustomFilter: () => void = useCallback((): void => {
    setCustomFilterEnabled(!isCustomFilterEnabled);
  }, [isCustomFilterEnabled, setCustomFilterEnabled]);

  // // GraphQL operations
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
      bePresent: formatBePresent(filterGroupToeInputTable.bePresent),
      canGetAttackedAt,
      canGetAttackedBy,
      canGetBePresentUntil,
      canGetFirstAttackAt,
      canGetSeenFirstTimeBy,
      first: 150,
      groupName,
      rootId: formatRootId(filterGroupToeInputTable.rootId),
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
  const toeInputs: IToeInputData[] = toeInputsEdges.map(
    ({ node }): IToeInputData => ({
      ...node,
      attackedAt: formatOptionalDate(node.attackedAt),
      bePresentUntil: formatOptionalDate(node.bePresentUntil),
      firstAttackAt: formatOptionalDate(node.firstAttackAt),
      markedSeenFirstTimeBy: markSeenFirstTimeBy(node.seenFirstTimeBy),
      rootId: _.isNil(node.root) ? "" : node.root.id,
      rootNickname: _.isNil(node.root) ? "" : node.root.nickname,
      seenAt: formatOptionalDate(node.seenAt),
    })
  );

  const formatBoolean = (value: boolean): string =>
    value
      ? translate.t("group.toe.inputs.yes")
      : translate.t("group.toe.inputs.no");
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

  const headersToeInputsTable: IHeaderConfig[] = [
    {
      dataField: "rootNickname",
      header: translate.t("group.toe.inputs.root"),
      onSort,
      visible: checkedItems.rootNickname,
    },
    {
      dataField: "component",
      header: translate.t("group.toe.inputs.component"),
      onSort,
      visible: checkedItems.component,
    },
    {
      dataField: "entryPoint",
      header: translate.t("group.toe.inputs.entryPoint"),
      onSort,
      visible: checkedItems.entryPoint,
    },
    {
      dataField: "hasVulnerabilities",
      formatter: formatBoolean,
      header: translate.t("group.toe.inputs.hasVulnerabilities"),
      onSort,
      visible: checkedItems.hasVulnerabilities,
    },
    {
      dataField: "attackedAt",
      filter: dateFilter({}),
      formatter: formatDate,
      header: translate.t("group.toe.inputs.attackedAt"),
      omit: !isInternal || !canGetAttackedAt,
      onSort,
      visible: checkedItems.attackedAt,
    },
    {
      dataField: "attackedBy",
      header: translate.t("group.toe.inputs.attackedBy"),
      omit: !isInternal || !canGetAttackedBy,
      onSort,
      visible: checkedItems.attackedBy,
    },
    {
      dataField: "firstAttackAt",
      filter: dateFilter({}),
      formatter: formatDate,
      header: translate.t("group.toe.inputs.firstAttackAt"),
      omit: !isInternal || !canGetFirstAttackAt,
      onSort,
      visible: checkedItems.firstAttackAt,
    },
    {
      dataField: "seenAt",
      filter: dateFilter({}),
      formatter: formatDate,
      header: translate.t("group.toe.inputs.seenAt"),
      onSort,
      visible: checkedItems.seenAt,
    },
    {
      dataField: "seenFirstTimeBy",
      header: translate.t("group.toe.inputs.seenFirstTimeBy"),
      omit: !isInternal || !canGetSeenFirstTimeBy,
      onSort,
      visible: checkedItems.seenFirstTimeBy,
    },
    {
      dataField: "bePresent",
      formatter: formatBoolean,
      header: translate.t("group.toe.inputs.bePresent"),
      onSort,
      visible: checkedItems.bePresent,
    },
    {
      dataField: "bePresentUntil",
      filter: dateFilter({}),
      formatter: formatDate,
      header: translate.t("group.toe.inputs.bePresentUntil"),
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
  function toggleEdit(): void {
    setIsEditing(!isEditing);
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
      placeholder: translate.t("group.toe.inputs.filters.root.placeholder"),
      selectOptions: rootSelectOptions,
      tooltipId: "group.toe.inputs.filters.root.tooltip.id",
      tooltipMessage: "group.toe.inputs.filters.root.tooltip",
      type: "select",
    },
    {
      defaultValue: filterGroupToeInputTable.component,
      onChangeSelect: onBasicFilterValueChange("component"),
      placeholder: translate.t(
        "group.toe.inputs.filters.component.placeholder"
      ),
      selectOptions: componentSelectOptions,
      tooltipId: "group.toe.inputs.filters.component.tooltip.id",
      tooltipMessage: "group.toe.inputs.filters.component.tooltip",
      translateSelectOptions: false,
      type: "select",
    },
    {
      defaultValue: filterGroupToeInputTable.hasVulnerabilities,
      onChangeSelect: onBasicFilterValueChange("hasVulnerabilities"),
      placeholder: translate.t(
        "group.toe.inputs.filters.hasVulnerabilities.placeholder"
      ),
      selectOptions: booleanSelectOptions,
      tooltipId: "group.toe.inputs.filters.hasVulnerabilities.tooltip.id",
      tooltipMessage: "group.toe.inputs.filters.hasVulnerabilities.tooltip",
      type: "select",
    },
    {
      defaultValue: "",
      placeholder: translate.t("group.toe.inputs.filters.seenAt.placeholder"),
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
      placeholder: translate.t(
        "group.toe.inputs.filters.seenFirstTimeBy.placeholder"
      ),
      selectOptions: seenFirstTimeBySelectOptions,
      tooltipId: "group.toe.inputs.filters.seenFirstTimeBy.tooltip.id",
      tooltipMessage: "group.toe.inputs.filters.seenFirstTimeBy.tooltip",
      type: "select",
    },
    {
      defaultValue: filterGroupToeInputTable.bePresent,
      onChangeSelect: onBasicFilterValueChange("bePresent"),
      placeholder: translate.t(
        "group.toe.inputs.filters.bePresent.placeholder"
      ),
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
    nonSelectable: undefined,
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
          _.get(sessionStorage, "toeInputsSort", initialSort)
        )}
        exportCsv={true}
        extraButtonsRight={
          <ActionButtons
            areInputsSelected={selectedToeInputDatas.length > 0}
            isAdding={isAdding}
            isEditing={isEditing}
            isInternal={isInternal}
            onAdd={toggleAdd}
            onEdit={toggleEdit}
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
      {isEditing ? (
        <HandleEditionModal
          groupName={groupName}
          handleCloseModal={toggleEdit}
          refetchData={refetch}
          selectedToeInputDatas={selectedToeInputDatas}
          setSelectedToeInputDatas={setSelectedToeInputDatas}
        />
      ) : undefined}
    </React.StrictMode>
  );
};

export { GroupToeInputsView };
