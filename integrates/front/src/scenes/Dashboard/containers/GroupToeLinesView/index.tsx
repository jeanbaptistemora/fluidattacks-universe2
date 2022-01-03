import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import moment from "moment";
import React, { useCallback, useEffect, useState } from "react";
import type { SortOrder } from "react-bootstrap-table-next";
import { dateFilter } from "react-bootstrap-table2-filter";
import { useParams } from "react-router-dom";

import { ActionButtons } from "./ActionButtons";
import { HandleEditionModal } from "./HandleEditionModal";
import {
  getNonSelectable,
  getToeLinesIndex,
  onSelectSeveralToeLinesHelper,
} from "./utils";

import { DataTableNext } from "components/DataTableNext";
import { commitFormatter } from "components/DataTableNext/formatters";
import type {
  IHeaderConfig,
  ISelectRowProps,
} from "components/DataTableNext/types";
import { filterSearchText } from "components/DataTableNext/utils";
import { GET_TOE_LINES } from "scenes/Dashboard/containers/GroupToeLinesView/queries";
import type {
  IGroupToeLinesViewProps,
  IToeLinesAttr,
  IToeLinesConnection,
  IToeLinesData,
  IToeLinesEdge,
} from "scenes/Dashboard/containers/GroupToeLinesView/types";
import { authzPermissionsContext } from "utils/authz/config";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { translate } from "utils/translations/translate";

const GroupToeLinesView: React.FC<IGroupToeLinesViewProps> = (
  props: IGroupToeLinesViewProps
): JSX.Element => {
  const { isInternal } = props;

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
  const [isEditing, setEditing] = useState(false);
  const [checkedItems, setCheckedItems] = useStoredState<
    Record<string, boolean>
  >(
    "toeLinesTableSet",
    {
      attackedAt: true,
      attackedBy: false,
      attackedLines: true,
      bePresent: true,
      bePresentUntil: false,
      comments: true,
      commitAuthor: false,
      coverage: true,
      daysToAttack: false,
      filename: false,
      firstAttackAt: false,
      loc: true,
      modifiedCommit: true,
      modifiedDate: true,
      rootNickname: true,
      seenAt: false,
      sortsRiskLevel: false,
    },
    localStorage
  );
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

  const [isFilterEnabled, setFilterEnabled] = useStoredState<boolean>(
    "toeLinesFilters",
    false
  );
  const [searchTextFilter, setSearchTextFilter] = useState("");
  const [selectedToeLinesDatas, setSelectedToeLinesDatas] = useState<
    IToeLinesData[]
  >([]);
  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }
  const handleUpdateFilter: () => void = useCallback((): void => {
    setFilterEnabled(!isFilterEnabled);
  }, [isFilterEnabled, setFilterEnabled]);
  function toggleEdit(): void {
    setEditing(!isEditing);
  }

  const formatDate: (date: Date | undefined) => string = (
    date: Date | undefined
  ): string => {
    if (_.isUndefined(date)) {
      return "";
    }

    return moment(date).format("YYYY-MM-DD");
  };
  const formatPercentage = (value: number): string =>
    new Intl.NumberFormat("en-IN", {
      style: "percent",
    }).format(value);
  const formatBoolean = (value: boolean): string =>
    value
      ? translate.t("group.toe.lines.yes")
      : translate.t("group.toe.lines.no");
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
      align: "center",
      dataField: "rootNickname",
      header: translate.t("group.toe.lines.root"),
      onSort,
      visible: checkedItems.rootNickname,
    },
    {
      align: "left",
      dataField: "filename",
      header: translate.t("group.toe.lines.filename"),
      onSort,
      visible: checkedItems.filename,
    },
    {
      align: "center",
      dataField: "coverage",
      formatter: formatPercentage,
      header: translate.t("group.toe.lines.coverage"),
      omit: !isInternal || !canSeeCoverage || !canGetAttackedLines,
      onSort,
      visible: checkedItems.coverage,
    },
    {
      align: "center",
      dataField: "loc",
      header: translate.t("group.toe.lines.loc"),
      onSort,
      visible: checkedItems.loc,
    },
    {
      align: "center",
      dataField: "attackedLines",
      header: translate.t("group.toe.lines.attackedLines"),
      omit: !isInternal || !canGetAttackedLines,
      onSort,
      visible: checkedItems.attackedLines,
    },
    {
      align: "center",
      dataField: "modifiedDate",
      filter: dateFilter({}),
      formatter: formatDate,
      header: translate.t("group.toe.lines.modifiedDate"),
      onSort,
      visible: checkedItems.modifiedDate,
    },
    {
      align: "center",
      dataField: "modifiedCommit",
      header: translate.t("group.toe.lines.modifiedCommit"),
      onSort,
      visible: checkedItems.modifiedCommit,
    },
    {
      align: "center",
      dataField: "commitAuthor",
      header: translate.t("group.toe.lines.commitAuthor"),
      onSort,
      visible: checkedItems.commitAuthor,
    },
    {
      align: "center",
      dataField: "daysToAttack",
      header: translate.t("group.toe.lines.daysToAttack"),
      omit: !isInternal || !canSeeDaysToAttack || !canGetAttackedAt,
      onSort,
      visible: checkedItems.daysToAttack,
    },
    {
      align: "center",
      dataField: "attackedAt",
      filter: dateFilter({}),
      formatter: formatDate,
      header: translate.t("group.toe.lines.attackedAt"),
      omit: !isInternal || !canGetAttackedAt,
      onSort,
      visible: checkedItems.attackedAt,
    },
    {
      align: "center",
      dataField: "attackedBy",
      header: translate.t("group.toe.lines.attackedBy"),
      omit: !isInternal || !canGetAttackedBy,
      onSort,
      visible: checkedItems.attackedBy,
    },
    {
      align: "center",
      dataField: "firstAttackAt",
      filter: dateFilter({}),
      formatter: formatDate,
      header: translate.t("group.toe.lines.firstAttackAt"),
      omit: !isInternal || !canGetFirstAttackAt,
      onSort,
      visible: checkedItems.firstAttackAt,
    },
    {
      align: "center",
      dataField: "seenAt",
      filter: dateFilter({}),
      formatter: formatDate,
      header: translate.t("group.toe.lines.seenAt"),
      onSort,
      visible: checkedItems.seenAt,
    },
    {
      align: "left",
      dataField: "comments",
      header: translate.t("group.toe.lines.comments"),
      omit: !isInternal || !canGetComments,
      onSort,
      visible: checkedItems.comments,
    },
    {
      align: "center",
      dataField: "sortsRiskLevel",
      formatter: formatRiskLevel,
      header: translate.t("group.toe.lines.sortsRiskLevel"),
      onSort,
      visible: checkedItems.sortsRiskLevel,
    },
    {
      align: "center",
      dataField: "bePresent",
      formatter: formatBoolean,
      header: translate.t("group.toe.lines.bePresent"),
      onSort,
      visible: checkedItems.bePresent,
    },
    {
      align: "center",
      dataField: "bePresentUntil",
      filter: dateFilter({}),
      formatter: formatDate,
      header: translate.t("group.toe.lines.bePresentUntil"),
      omit: !isInternal || !canGetBePresentUntil,
      onSort,
      visible: checkedItems.bePresentUntil,
    },
  ];

  // // GraphQL operations
  const { data, fetchMore, refetch } = useQuery<{
    group: { toeLines: IToeLinesConnection };
  }>(GET_TOE_LINES, {
    fetchPolicy: "cache-first",
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load group toe lines", error);
      });
    },
    variables: {
      canGetAttackedAt,
      canGetAttackedBy,
      canGetAttackedLines,
      canGetBePresentUntil,
      canGetComments,
      canGetFirstAttackAt,
      first: 300,
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
      firstAttackAt: formatOptionalDate(node.firstAttackAt),
      modifiedCommit: commitFormatter(node.modifiedCommit),
      modifiedDate: formatOptionalDate(node.modifiedDate),
      rootId: node.root.id,
      rootNickname: node.root.nickname,
      seenAt: formatOptionalDate(node.seenAt),
    })
  );
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

  const filterSearchtextResult: IToeLinesData[] = filterSearchText(
    toeLines,
    searchTextFilter
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const initialSort: string = JSON.stringify({
    dataField: "rootNickname",
    order: "asc",
  });

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
    nonSelectable: getNonSelectable(toeLines),
    onSelect: onSelectOneToeLinesData,
    onSelectAll: onSelectSeveralToeLinesDatas,
    selected: getToeLinesIndex(selectedToeLinesDatas, toeLines),
  };

  return (
    <React.StrictMode>
      <DataTableNext
        bordered={true}
        columnToggle={true}
        customSearch={{
          customSearchDefault: searchTextFilter,
          isCustomSearchEnabled: true,
          onUpdateCustomSearch: onSearchTextChange,
          position: "right",
        }}
        dataset={filterSearchtextResult}
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
        isFilterEnabled={isFilterEnabled}
        onColumnToggle={handleChange}
        onUpdateEnableFilter={handleUpdateFilter}
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
        />
      ) : undefined}
    </React.StrictMode>
  );
};

export { GroupToeLinesView };
