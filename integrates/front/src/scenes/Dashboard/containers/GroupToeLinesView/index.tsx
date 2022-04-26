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
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { ActionButtons } from "./ActionButtons";
import { HandleEditionModal } from "./HandleEditionModal";
import {
  formatBePresent,
  formatPercentage,
  formatRootId,
  getFilteredData,
  getNonSelectable,
  getToeLinesIndex,
  onSelectSeveralToeLinesHelper,
} from "./utils";

import { Table } from "components/Table";
import { commitFormatter } from "components/Table/formatters";
import type {
  IFilterProps,
  IHeaderConfig,
  ISelectRowProps,
} from "components/Table/types";
import { GET_TOE_LINES } from "scenes/Dashboard/containers/GroupToeLinesView/queries";
import type {
  IFilterSet,
  IGroupToeLinesViewProps,
  IToeLinesAttr,
  IToeLinesConnection,
  IToeLinesData,
  IToeLinesEdge,
} from "scenes/Dashboard/containers/GroupToeLinesView/types";
import { GET_ROOT_IDS } from "scenes/Dashboard/queries";
import type { IGroupRootIdsAttr, IRootIdAttr } from "scenes/Dashboard/types";
import { authzPermissionsContext } from "utils/authz/config";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";

const NOEXTENSION = ".no.extension.";

const GroupToeLinesView: React.FC<IGroupToeLinesViewProps> = ({
  isInternal,
}: IGroupToeLinesViewProps): JSX.Element => {
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateAttackedLines: boolean = permissions.can(
    "api_mutations_update_toe_lines_attacked_lines_mutate"
  );
  const canGetAttackedAt: boolean = permissions.can(
    "api_resolvers_toe_lines_attacked_at_resolve"
  );
  const canGetAttackedBy: boolean = permissions.can(
    "api_resolvers_toe_lines_attacked_by_resolve"
  );
  const canGetAttackedLines: boolean = permissions.can(
    "api_resolvers_toe_lines_attacked_lines_resolve"
  );
  const canGetBePresentUntil: boolean = permissions.can(
    "api_resolvers_toe_lines_be_present_until_resolve"
  );
  const canGetComments: boolean = permissions.can(
    "api_resolvers_toe_lines_comments_resolve"
  );
  const canGetFirstAttackAt: boolean = permissions.can(
    "api_resolvers_toe_lines_first_attack_at_resolve"
  );
  const canSeeCoverage: boolean = permissions.can("see_toe_lines_coverage");
  const canSeeDaysToAttack: boolean = permissions.can(
    "see_toe_lines_days_to_attack"
  );

  const { groupName } = useParams<{ groupName: string }>();

  const [isEditing, setIsEditing] = useState(false);
  const [searchTextFilter, setSearchTextFilter] = useState("");
  const [selectedToeLinesDatas, setSelectedToeLinesDatas] = useState<
    IToeLinesData[]
  >([]);

  const [checkedItems, setCheckedItems] = useStoredState<
    Record<string, boolean>
  >(
    "toeLinesTableSet",
    {
      attackedAt: true,
      attackedBy: false,
      attackedLines: true,
      bePresent: false,
      bePresentUntil: false,
      comments: true,
      coverage: true,
      daysToAttack: false,
      filename: false,
      firstAttackAt: false,
      hasVulnerabilities: true,
      lastAuthor: false,
      lastCommit: true,
      loc: true,
      modifiedDate: true,
      rootNickname: true,
      seenAt: false,
      sortsRiskLevel: false,
    },
    localStorage
  );
  const [filterGroupToeLinesTable, setFilterGroupToeLinesTable] =
    useStoredState<IFilterSet>(
      `filterGroupToeLinesSet-${groupName}`,
      {
        bePresent: "",
        coverage: { max: "", min: "" },
        filenameExtension: "",
        hasVulnerabilities: "",
        modifiedDate: { max: "", min: "" },
        priority: { max: "", min: "" },
        rootId: "",
        seenAt: { max: "", min: "" },
      },
      localStorage
    );
  const [isCustomFilterEnabled, setCustomFilterEnabled] =
    useStoredState<boolean>("toeLinesCustomFilters", false);

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

  const formatDate: (date: Date | undefined) => string = (
    date: Date | undefined
  ): string => {
    if (_.isUndefined(date)) {
      return "";
    }

    return moment(date).format("YYYY-MM-DD");
  };
  const formatBoolean = (value: boolean): string =>
    value ? t("group.toe.lines.yes") : t("group.toe.lines.no");
  const onSort: (dataField: string, order: SortOrder) => void = (
    dataField: string,
    order: SortOrder
  ): void => {
    const newSorted = { dataField, order };
    sessionStorage.setItem("toeLinesSort", JSON.stringify(newSorted));
  };
  const formatRiskLevel = (sortsRiskLevel: number): string =>
    sortsRiskLevel >= 0 ? `${sortsRiskLevel.toString()} %` : "n/a";

  const headersToeLinesTable: IHeaderConfig[] = [
    {
      dataField: "rootNickname",
      header: t("group.toe.lines.root"),
      onSort,
      visible: checkedItems.rootNickname,
    },
    {
      dataField: "filename",
      header: t("group.toe.lines.filename"),
      onSort,
      visible: checkedItems.filename,
    },
    {
      dataField: "coverage",
      formatter: formatPercentage,
      header: t("group.toe.lines.coverage"),
      omit: !isInternal || !canSeeCoverage || !canGetAttackedLines,
      onSort,
      visible: checkedItems.coverage,
    },
    {
      dataField: "loc",
      header: t("group.toe.lines.loc"),
      onSort,
      visible: checkedItems.loc,
    },
    {
      dataField: "attackedLines",
      header: t("group.toe.lines.attackedLines"),
      omit: !isInternal || !canGetAttackedLines,
      onSort,
      visible: checkedItems.attackedLines,
    },
    {
      dataField: "hasVulnerabilities",
      formatter: formatBoolean,
      header: t("group.toe.lines.hasVulnerabilities"),
      onSort,
      visible: checkedItems.hasVulnerabilities,
    },
    {
      dataField: "modifiedDate",
      filter: dateFilter({}),
      formatter: formatDate,
      header: t("group.toe.lines.modifiedDate"),
      onSort,
      visible: checkedItems.modifiedDate,
    },
    {
      dataField: "lastCommit",
      header: t("group.toe.lines.lastCommit"),
      onSort,
      visible: checkedItems.lastCommit,
    },
    {
      dataField: "lastAuthor",
      header: t("group.toe.lines.lastAuthor"),
      onSort,
      visible: checkedItems.lastAuthor,
    },
    {
      dataField: "daysToAttack",
      header: t("group.toe.lines.daysToAttack"),
      omit: !isInternal || !canSeeDaysToAttack || !canGetAttackedAt,
      onSort,
      visible: checkedItems.daysToAttack,
    },
    {
      dataField: "attackedAt",
      filter: dateFilter({}),
      formatter: formatDate,
      header: t("group.toe.lines.attackedAt"),
      omit: !isInternal || !canGetAttackedAt,
      onSort,
      visible: checkedItems.attackedAt,
    },
    {
      dataField: "attackedBy",
      header: t("group.toe.lines.attackedBy"),
      omit: !isInternal || !canGetAttackedBy,
      onSort,
      visible: checkedItems.attackedBy,
    },
    {
      dataField: "firstAttackAt",
      filter: dateFilter({}),
      formatter: formatDate,
      header: t("group.toe.lines.firstAttackAt"),
      omit: !isInternal || !canGetFirstAttackAt,
      onSort,
      visible: checkedItems.firstAttackAt,
    },
    {
      dataField: "seenAt",
      filter: dateFilter({}),
      formatter: formatDate,
      header: t("group.toe.lines.seenAt"),
      onSort,
      visible: checkedItems.seenAt,
    },
    {
      dataField: "comments",
      header: t("group.toe.lines.comments"),
      omit: !isInternal || !canGetComments,
      onSort,
      visible: checkedItems.comments,
    },
    {
      dataField: "sortsRiskLevel",
      formatter: formatRiskLevel,
      header: t("group.toe.lines.sortsRiskLevel"),
      onSort,
      visible: checkedItems.sortsRiskLevel,
    },
    {
      dataField: "bePresent",
      formatter: formatBoolean,
      header: t("group.toe.lines.bePresent"),
      onSort,
      visible: checkedItems.bePresent,
    },
    {
      dataField: "bePresentUntil",
      filter: dateFilter({}),
      formatter: formatDate,
      header: t("group.toe.lines.bePresentUntil"),
      omit: !isInternal || !canGetBePresentUntil,
      onSort,
      visible: checkedItems.bePresentUntil,
    },
  ];

  // // GraphQL operations
  const { data, fetchMore, refetch } = useQuery<{
    group: { toeLines: IToeLinesConnection };
  }>(GET_TOE_LINES, {
    fetchPolicy: "network-only",
    nextFetchPolicy: "cache-first",
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load group toe lines", error);
      });
    },
    variables: {
      bePresent: formatBePresent(filterGroupToeLinesTable.bePresent),
      canGetAttackedAt,
      canGetAttackedBy,
      canGetAttackedLines,
      canGetBePresentUntil,
      canGetComments,
      canGetFirstAttackAt,
      first: 150,
      groupName,
      rootId: formatRootId(filterGroupToeLinesTable.rootId),
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
    data === undefined ? undefined : data.group.toeLines.pageInfo;
  const toeLinesEdges: IToeLinesEdge[] =
    data === undefined ? [] : data.group.toeLines.edges;
  const getCoverage = (toeLinesAttr: IToeLinesAttr): number =>
    toeLinesAttr.loc === 0 ? 1 : toeLinesAttr.attackedLines / toeLinesAttr.loc;
  const getDaysToAttack = (toeLinesAttr: IToeLinesAttr): number =>
    _.isNull(toeLinesAttr.attackedAt) ||
    _.isEmpty(toeLinesAttr.attackedAt) ||
    moment(toeLinesAttr.modifiedDate) > moment(toeLinesAttr.attackedAt)
      ? toeLinesAttr.bePresent
        ? moment().diff(moment(toeLinesAttr.modifiedDate), "days")
        : moment(toeLinesAttr.bePresentUntil).diff(
            moment(toeLinesAttr.modifiedDate),
            "days"
          )
      : moment(toeLinesAttr.attackedAt).diff(
          moment(toeLinesAttr.modifiedDate),
          "days"
        );
  const getExtension = (toeLinesAttr: IToeLinesAttr): string => {
    const lastPointindex = toeLinesAttr.filename.lastIndexOf(".");
    const lastSlashIndex = toeLinesAttr.filename.lastIndexOf("/");
    if (lastPointindex === -1 || lastSlashIndex > lastPointindex) {
      return NOEXTENSION;
    }

    return toeLinesAttr.filename.slice(lastPointindex + 1);
  };

  const formatOptionalDate: (date: string | null) => Date | undefined = (
    date: string | null
  ): Date | undefined =>
    _.isNull(date) || _.isEmpty(date) ? undefined : new Date(date);
  const toeLines: IToeLinesData[] = toeLinesEdges.map(
    ({ node }): IToeLinesData => ({
      ...node,
      attackedAt: formatOptionalDate(node.attackedAt),
      bePresentUntil: formatOptionalDate(node.bePresentUntil),
      coverage: getCoverage(node),
      daysToAttack: getDaysToAttack(node),
      extension: getExtension(node),
      firstAttackAt: formatOptionalDate(node.firstAttackAt),
      lastCommit: commitFormatter(node.lastCommit),
      modifiedDate: formatOptionalDate(node.modifiedDate),
      rootId: node.root.id,
      rootNickname: node.root.nickname,
      seenAt: formatOptionalDate(node.seenAt),
    })
  );

  const roots = rootIdsData === undefined ? [] : rootIdsData.group.roots;
  function clearFilters(): void {
    setFilterGroupToeLinesTable(
      (): IFilterSet => ({
        bePresent: "",
        coverage: { max: "", min: "" },
        filenameExtension: "",
        hasVulnerabilities: "",
        modifiedDate: { max: "", min: "" },
        priority: { max: "", min: "" },
        rootId: "",
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
    setSelectedToeLinesDatas([]);
    void refetch();
  }, [
    filterGroupToeLinesTable.bePresent,
    filterGroupToeLinesTable.rootId,
    refetch,
  ]);

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  function toggleEdit(): void {
    setIsEditing(!isEditing);
  }

  const onBasicFilterValueChange = (
    filterName: keyof IFilterSet
  ): ((event: ChangeEvent<HTMLSelectElement>) => void) => {
    return (event: React.ChangeEvent<HTMLSelectElement>): void => {
      event.persist();
      setFilterGroupToeLinesTable(
        (value): IFilterSet => ({
          ...value,
          [filterName]: event.target.value,
        })
      );
    };
  };
  const onRangeFilterValueChange = (
    filterName: keyof Pick<
      IFilterSet,
      "coverage" | "modifiedDate" | "priority" | "seenAt"
    >,
    key: "max" | "min"
  ): ((event: ChangeEvent<HTMLInputElement>) => void) => {
    return (event: React.ChangeEvent<HTMLInputElement>): void => {
      event.persist();

      setFilterGroupToeLinesTable(
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

  const extensionSelectOptions = Object.fromEntries(
    toeLines
      .map((toeLinesData: IToeLinesData): string[] => [
        toeLinesData.extension,
        toeLinesData.extension,
      ])
      // Can also be string[] but the unknown type overrides it
      .map(([key, val]): unknown[] => [key, val === NOEXTENSION ? "" : val])
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
  const customFiltersProps: IFilterProps[] = [
    {
      defaultValue: filterGroupToeLinesTable.rootId,
      onChangeSelect: onBasicFilterValueChange("rootId"),
      placeholder: t("group.toe.lines.filters.root.placeholder"),
      selectOptions: rootSelectOptions,
      tooltipId: "group.toe.lines.filters.root.tooltip.id",
      tooltipMessage: "group.toe.lines.filters.root.tooltip",
      type: "select",
    },
    {
      defaultValue: filterGroupToeLinesTable.filenameExtension,
      onChangeSelect: onBasicFilterValueChange("filenameExtension"),
      placeholder: t("group.toe.lines.filters.extension.placeholder"),
      selectOptions: extensionSelectOptions,
      tooltipId: "group.toe.lines.filters.extension.tooltip.id",
      tooltipMessage: "group.toe.lines.filters.extension.tooltip",
      type: "select",
    },
    {
      defaultValue: "",
      omit: !isInternal || !canSeeCoverage || !canGetAttackedLines,
      placeholder: t("group.toe.lines.filters.coverage.placeholder"),
      rangeProps: {
        defaultValue: filterGroupToeLinesTable.coverage,
        onChangeMax: onRangeFilterValueChange("coverage", "max"),
        onChangeMin: onRangeFilterValueChange("coverage", "min"),
        step: 1,
      },
      tooltipId: "group.toe.lines.filters.coverage.tooltip.id",
      tooltipMessage: "group.toe.lines.filters.coverage.tooltip",
      type: "range",
    },
    {
      defaultValue: "",
      placeholder: t("group.toe.lines.filters.modifiedDate.placeholder"),
      rangeProps: {
        defaultValue: filterGroupToeLinesTable.modifiedDate,
        onChangeMax: onRangeFilterValueChange("modifiedDate", "max"),
        onChangeMin: onRangeFilterValueChange("modifiedDate", "min"),
      },
      tooltipId: "group.toe.lines.filters.modifiedDate.tooltip.id",
      tooltipMessage: "group.toe.lines.filters.modifiedDate.tooltip",
      type: "dateRange",
    },
    {
      defaultValue: filterGroupToeLinesTable.hasVulnerabilities,
      onChangeSelect: onBasicFilterValueChange("hasVulnerabilities"),
      placeholder: t("group.toe.lines.filters.hasVulnerabilities.placeholder"),
      selectOptions: booleanSelectOptions,
      tooltipId: "group.toe.lines.filters.hasVulnerabilities.tooltip.id",
      tooltipMessage: "group.toe.lines.filters.hasVulnerabilities.tooltip",
      type: "select",
    },
    {
      defaultValue: "",
      placeholder: t("group.toe.lines.filters.seenAt.placeholder"),
      rangeProps: {
        defaultValue: filterGroupToeLinesTable.seenAt,
        onChangeMax: onRangeFilterValueChange("seenAt", "max"),
        onChangeMin: onRangeFilterValueChange("seenAt", "min"),
      },
      tooltipId: "group.toe.lines.filters.seenAt.tooltip.id",
      tooltipMessage: "group.toe.lines.filters.seenAt.tooltip",
      type: "dateRange",
    },
    {
      defaultValue: "",
      placeholder: t("group.toe.lines.filters.priority.placeholder"),
      rangeProps: {
        defaultValue: filterGroupToeLinesTable.priority,
        onChangeMax: onRangeFilterValueChange("priority", "max"),
        onChangeMin: onRangeFilterValueChange("priority", "min"),
        step: 1,
      },
      tooltipId: "group.toe.lines.filters.priority.tooltip.id",
      tooltipMessage: "group.toe.lines.filters.priority.tooltip",
      type: "range",
    },
    {
      defaultValue: filterGroupToeLinesTable.bePresent,
      onChangeSelect: onBasicFilterValueChange("bePresent"),
      placeholder: t("group.toe.lines.filters.bePresent.placeholder"),
      selectOptions: booleanSelectOptions,
      tooltipId: "group.toe.lines.filters.bePresent.tooltip.id",
      tooltipMessage: "group.toe.lines.filters.bePresent.tooltip",
      type: "select",
    },
  ];
  const filteredData: IToeLinesData[] = getFilteredData(
    filterGroupToeLinesTable,
    searchTextFilter,
    toeLines
  );

  function onSelectSeveralToeLinesDatas(
    isSelect: boolean,
    toeLinesDatasSelected: IToeLinesData[]
  ): string[] {
    return onSelectSeveralToeLinesHelper(
      isSelect,
      toeLinesDatasSelected,
      selectedToeLinesDatas,
      setSelectedToeLinesDatas
    );
  }
  function onSelectOneToeLinesData(
    toeLinesdata: IToeLinesData,
    isSelect: boolean
  ): boolean {
    onSelectSeveralToeLinesDatas(isSelect, [toeLinesdata]);

    return true;
  }
  const selectionMode: ISelectRowProps = {
    clickToSelect: false,
    hideSelectColumn: !isInternal || !canUpdateAttackedLines,
    mode: "checkbox",
    nonSelectable: getNonSelectable(filteredData),
    onSelect: onSelectOneToeLinesData,
    onSelectAll: onSelectSeveralToeLinesDatas,
    selected: getToeLinesIndex(selectedToeLinesDatas, filteredData),
  };

  const initialSort: string = JSON.stringify({
    dataField: "rootNickname",
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
          _.get(sessionStorage, "toeLinesSort", initialSort)
        )}
        exportCsv={true}
        extraButtonsRight={
          <ActionButtons
            areToeLinesDatasSelected={selectedToeLinesDatas.length > 0}
            isEditing={isEditing}
            isInternal={isInternal}
            onEdit={toggleEdit}
          />
        }
        headers={headersToeLinesTable}
        id={"tblToeLines"}
        isFilterEnabled={undefined}
        onColumnToggle={handleChange}
        pageSize={100}
        search={false}
        selectionMode={selectionMode}
      />
      {isEditing ? (
        <HandleEditionModal
          groupName={groupName}
          handleCloseModal={toggleEdit}
          refetchData={refetch}
          selectedToeLinesDatas={selectedToeLinesDatas}
          setSelectedToeLinesDatas={setSelectedToeLinesDatas}
        />
      ) : undefined}
    </React.StrictMode>
  );
};

export { GroupToeLinesView };
