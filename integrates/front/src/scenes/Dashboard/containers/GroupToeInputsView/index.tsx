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
  getFilteredData,
  getToeInputIndex,
  onSelectSeveralToeInputHelper,
} from "./utils";

import { DataTableNext } from "components/DataTableNext";
import type {
  IFilterProps,
  IHeaderConfig,
  ISelectRowProps,
} from "components/DataTableNext/types";
import { GET_TOE_INPUTS } from "scenes/Dashboard/containers/GroupToeInputsView/queries";
import type {
  IFilterSet,
  IGroupToeInputsViewProps,
  IToeInputData,
  IToeInputEdge,
  IToeInputsConnection,
} from "scenes/Dashboard/containers/GroupToeInputsView/types";
import { authzPermissionsContext } from "utils/authz/config";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { translate } from "utils/translations/translate";

const NOROOT = "no root";

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
      seenAt: true,
      seenFirstTimeBy: true,
      unreliableRootNickname: true,
    },
    localStorage
  );
  const [filterGroupToeInputTable, setFilterGroupToeInputTable] =
    useStoredState<IFilterSet>(
      "filterGroupToeInputSet",
      {
        bePresent: "",
        component: "",
        hasVulnerabilities: "",
        root: "",
        seenAt: { max: "", min: "" },
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
    fetchPolicy: "cache-first",
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load toe inputs", error);
      });
    },
    variables: {
      canGetAttackedAt,
      canGetAttackedBy,
      canGetBePresentUntil,
      canGetFirstAttackAt,
      canGetSeenFirstTimeBy,
      first: 300,
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
  const markNickname: (rootNickname: string) => string = (
    rootNickname: string
  ): string => (_.isEmpty(rootNickname) ? NOROOT : rootNickname);
  const toeInputs: IToeInputData[] = toeInputsEdges.map(
    ({ node }): IToeInputData => ({
      ...node,
      attackedAt: formatOptionalDate(node.attackedAt),
      bePresentUntil: formatOptionalDate(node.bePresentUntil),
      firstAttackAt: formatOptionalDate(node.firstAttackAt),
      markedRootNickname: markNickname(node.unreliableRootNickname),
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
      align: "center",
      dataField: "unreliableRootNickname",
      header: translate.t("group.toe.inputs.root"),
      onSort,
      visible: checkedItems.unreliableRootNickname,
    },
    {
      align: "left",
      dataField: "component",
      header: translate.t("group.toe.inputs.component"),
      onSort,
      visible: checkedItems.component,
    },
    {
      align: "left",
      dataField: "entryPoint",
      header: translate.t("group.toe.inputs.entryPoint"),
      onSort,
      visible: checkedItems.entryPoint,
    },
    {
      align: "center",
      dataField: "hasVulnerabilities",
      formatter: formatBoolean,
      header: translate.t("group.toe.inputs.hasVulnerabilities"),
      onSort,
      visible: checkedItems.hasVulnerabilities,
    },
    {
      align: "center",
      dataField: "attackedAt",
      filter: dateFilter({}),
      formatter: formatDate,
      header: translate.t("group.toe.inputs.attackedAt"),
      omit: !isInternal || !canGetAttackedAt,
      onSort,
      visible: checkedItems.attackedAt,
    },
    {
      align: "center",
      dataField: "attackedBy",
      header: translate.t("group.toe.inputs.attackedBy"),
      omit: !isInternal || !canGetAttackedBy,
      onSort,
      visible: checkedItems.attackedBy,
    },
    {
      align: "center",
      dataField: "firstAttackAt",
      filter: dateFilter({}),
      formatter: formatDate,
      header: translate.t("group.toe.inputs.firstAttackAt"),
      omit: !isInternal || !canGetFirstAttackAt,
      onSort,
      visible: checkedItems.firstAttackAt,
    },
    {
      align: "center",
      dataField: "seenAt",
      filter: dateFilter({}),
      formatter: formatDate,
      header: translate.t("group.toe.inputs.seenAt"),
      onSort,
      visible: checkedItems.seenAt,
    },
    {
      align: "left",
      dataField: "seenFirstTimeBy",
      header: translate.t("group.toe.inputs.seenFirstTimeBy"),
      omit: !isInternal || !canGetSeenFirstTimeBy,
      onSort,
      visible: checkedItems.seenFirstTimeBy,
    },
    {
      align: "center",
      dataField: "bePresent",
      formatter: formatBoolean,
      header: translate.t("group.toe.inputs.bePresent"),
      onSort,
      visible: checkedItems.bePresent,
    },
    {
      align: "center",
      dataField: "bePresentUntil",
      filter: dateFilter({}),
      formatter: formatDate,
      header: translate.t("group.toe.inputs.bePresentUntil"),
      omit: !isInternal || !canGetBePresentUntil,
      onSort,
      visible: checkedItems.bePresentUntil,
    },
  ];

  function clearFilters(): void {
    setFilterGroupToeInputTable(
      (): IFilterSet => ({
        bePresent: "",
        component: "",
        hasVulnerabilities: "",
        root: "",
        seenAt: { max: "", min: "" },
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
    if (!_.isUndefined(data)) {
      void refetch();
    }
    // It is important to run only during the first render
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  useEffect((): void => {
    clearFilters();
    // It is important to run only during the first render
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

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
    toeInputs.map((toeInputData: IToeInputData): string[] => [
      toeInputData.markedRootNickname,
      toeInputData.unreliableRootNickname,
    ])
  );
  const booleanSelectOptions = Object.fromEntries([
    ["false", formatBoolean(false)],
    ["true", formatBoolean(true)],
  ]);
  const customFiltersProps: IFilterProps[] = [
    {
      defaultValue: filterGroupToeInputTable.root,
      onChangeSelect: onBasicFilterValueChange("root"),
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
      <DataTableNext
        bordered={true}
        clearFiltersButton={clearFilters}
        columnToggle={true}
        customFilters={{
          customFiltersProps,
          isCustomFilterEnabled,
          onUpdateEnableCustomFilter: handleUpdateCustomFilter,
          oneRowMessage: true,
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
