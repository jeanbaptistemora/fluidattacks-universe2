import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import moment from "moment";
import React, { useCallback, useState } from "react";
import type { SortOrder } from "react-bootstrap-table-next";
import { dateFilter } from "react-bootstrap-table2-filter";
import { useParams } from "react-router-dom";

import { DataTableNext } from "components/DataTableNext";
import { commitFormatter } from "components/DataTableNext/formatters";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { filterSearchText } from "components/DataTableNext/utils";
import { GET_TOE_LINES } from "scenes/Dashboard/containers/GroupToeLinesView/queries";
import type {
  IToeLinesAttr,
  IToeLinesConnection,
  IToeLinesData,
  IToeLinesEdge,
} from "scenes/Dashboard/containers/GroupToeLinesView/types";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { translate } from "utils/translations/translate";

const GroupToeLinesView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();

  const [checkedItems, setCheckedItems] = useStoredState<
    Record<string, boolean>
  >(
    "toeLinesTableSet",
    {
      comments: true,
      coverage: true,
      filename: false,
      loc: true,
      modifiedCommit: true,
      modifiedDate: true,
      rootNickname: true,
      sortsRiskLevel: false,
      testedDate: true,
      testedLines: true,
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
  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }
  const handleUpdateFilter: () => void = useCallback((): void => {
    setFilterEnabled(!isFilterEnabled);
  }, [isFilterEnabled, setFilterEnabled]);

  const formatDate: (date: string) => string = (date: string): string => {
    const dateObj: Date = new Date(date);

    return moment(dateObj).format("YYYY-MM-DD");
  };
  const formatPercentage = (value: number): string =>
    new Intl.NumberFormat("en-IN", {
      style: "percent",
    }).format(value);
  const onSort: (dataField: string, order: SortOrder) => void = (
    dataField: string,
    order: SortOrder
  ): void => {
    const newSorted = { dataField, order };
    sessionStorage.setItem("toeLinesSort", JSON.stringify(newSorted));
  };

  const headersToeLinesTable: IHeaderConfig[] = [
    {
      align: "center",
      dataField: "rootNickname",
      header: translate.t("group.toe.lines.root"),
      onSort,
      visible: checkedItems.rootNickname,
      width: "10%",
    },
    {
      align: "left",
      dataField: "filename",
      header: translate.t("group.toe.lines.filename"),
      onSort,
      visible: checkedItems.filename,
      width: "40%",
    },
    {
      align: "center",
      dataField: "coverage",
      formatter: formatPercentage,
      header: translate.t("group.toe.lines.coverage"),
      onSort,
      visible: checkedItems.coverage,
      width: "2.5%",
    },
    {
      align: "center",
      dataField: "loc",
      header: translate.t("group.toe.lines.loc"),
      onSort,
      visible: checkedItems.loc,
      width: "8%",
    },
    {
      align: "center",
      dataField: "attackedLines",
      header: translate.t("group.toe.lines.testedLines"),
      onSort,
      visible: checkedItems.testedLines,
      width: "8%",
    },
    {
      align: "center",
      dataField: "modifiedDate",
      filter: dateFilter({}),
      formatter: formatDate,
      header: translate.t("group.toe.lines.modifiedDate"),
      onSort,
      visible: checkedItems.modifiedDate,
      width: "5%",
    },
    {
      align: "center",
      dataField: "modifiedCommit",
      header: translate.t("group.toe.lines.modifiedCommit"),
      onSort,
      visible: checkedItems.modifiedCommit,
      width: "10%",
    },
    {
      align: "center",
      dataField: "attackedAt",
      filter: dateFilter({}),
      formatter: formatDate,
      header: translate.t("group.toe.lines.testedDate"),
      onSort,
      visible: checkedItems.testedDate,
      width: "5%",
    },
    {
      align: "left",
      dataField: "comments",
      header: translate.t("group.toe.lines.comments"),
      onSort,
      visible: checkedItems.comments,
      width: "15%",
    },
    {
      align: "center",
      dataField: "sortsRiskLevel",
      header: translate.t("group.toe.lines.sortsRiskLevel"),
      onSort,
      visible: checkedItems.sortsRiskLevel,
      width: "2.5%",
    },
  ];

  // // GraphQL operations
  const { data } = useQuery<{
    group: { toeLines: IToeLinesConnection };
  }>(GET_TOE_LINES, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load group toe lines", error);
      });
    },
    variables: { bePresent: true, groupName },
  });
  const toeLinesEdges: IToeLinesEdge[] =
    data === undefined ? [] : data.group.toeLines.edges;
  const getCoverage = (toeLinesAttr: IToeLinesAttr): number =>
    toeLinesAttr.loc === 0 ? 1 : toeLinesAttr.attackedLines / toeLinesAttr.loc;
  const getSortsRiskLevel = (toeLinesAttr: IToeLinesAttr): string =>
    toeLinesAttr.sortsRiskLevel >= 0
      ? `${toeLinesAttr.sortsRiskLevel.toString()} %`
      : "n/a";
  const toeLines: IToeLinesData[] = toeLinesEdges.map(
    ({ node }): IToeLinesData => ({
      ...node,
      coverage: getCoverage(node),
      modifiedCommit: commitFormatter(node.modifiedCommit),
      rootNickname: node.root.nickname,
      sortsRiskLevel: getSortsRiskLevel(node),
    })
  );
  const filterSearchtextResult: IToeLinesData[] = filterSearchText(
    toeLines,
    searchTextFilter
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const initialSort: string = JSON.stringify({
    dataField: "filename",
    order: "asc",
  });

  return (
    <React.StrictMode>
      <DataTableNext
        bordered={true}
        columnToggle={true}
        customSearch={{
          customSearchDefault: searchTextFilter,
          isCustomSearchEnabled: true,
          onUpdateCustomSearch: onSearchTextChange,
        }}
        dataset={filterSearchtextResult}
        defaultSorted={JSON.parse(
          _.get(sessionStorage, "toeLinesSort", initialSort)
        )}
        exportCsv={true}
        headers={headersToeLinesTable}
        id={"tblToeLines"}
        isFilterEnabled={isFilterEnabled}
        onColumnToggle={handleChange}
        onUpdateEnableFilter={handleUpdateFilter}
        pageSize={100}
        search={false}
      />
    </React.StrictMode>
  );
};

export { GroupToeLinesView };
