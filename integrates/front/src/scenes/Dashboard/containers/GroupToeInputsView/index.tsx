import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import moment from "moment";
import React, { useCallback, useEffect, useState } from "react";
import type { SortOrder } from "react-bootstrap-table-next";
import { dateFilter } from "react-bootstrap-table2-filter";
import { useParams } from "react-router-dom";

import { DataTableNext } from "components/DataTableNext";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { filterSearchText } from "components/DataTableNext/utils";
import { GET_TOE_INPUTS } from "scenes/Dashboard/containers/GroupToeInputsView/queries";
import type {
  IToeInputData,
  IToeInputEdge,
  IToeInputsConnection,
} from "scenes/Dashboard/containers/GroupToeInputsView/types";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { translate } from "utils/translations/translate";

const GroupToeInputsView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();

  const [checkedItems, setCheckedItems] = useStoredState<
    Record<string, boolean>
  >(
    "toeInputsTableSet",
    {
      attackedAt: true,
      component: false,
      entryPoint: true,
      seenAt: true,
      seenFirstTimeBy: true,
      unreliableRootNickname: true,
    },
    localStorage
  );
  const [searchTextFilter, setSearchTextFilter] = useState("");
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
    "toeInputsFilters",
    false
  );
  const handleUpdateFilter: () => void = useCallback((): void => {
    setFilterEnabled(!isFilterEnabled);
  }, [isFilterEnabled, setFilterEnabled]);

  const formatDate: (date: string) => string = (date: string): string => {
    if (_.isEmpty(date)) {
      return "";
    }
    const dateObj: Date = new Date(date);

    return moment(dateObj).format("YYYY-MM-DD");
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
      width: "10%",
    },
    {
      align: "left",
      dataField: "component",
      header: translate.t("group.toe.inputs.component"),
      onSort,
      visible: checkedItems.component,
      width: "30%",
    },
    {
      align: "left",
      dataField: "entryPoint",
      header: translate.t("group.toe.inputs.entryPoint"),
      onSort,
      visible: checkedItems.entryPoint,
      width: "10%",
    },
    {
      align: "center",
      dataField: "attackedAt",
      filter: dateFilter({}),
      formatter: formatDate,
      header: translate.t("group.toe.inputs.testedDate"),
      onSort,
      visible: checkedItems.testedDate,
      width: "8%",
    },
    {
      align: "center",
      dataField: "seenAt",
      filter: dateFilter({}),
      formatter: formatDate,
      header: translate.t("group.toe.inputs.createdDate"),
      onSort,
      visible: checkedItems.createdDate,
      width: "8%",
    },
    {
      align: "left",
      dataField: "seenFirstTimeBy",
      header: translate.t("group.toe.inputs.seenFirstTimeBy"),
      onSort,
      visible: checkedItems.seenFirstTimeBy,
      width: "15%",
    },
  ];

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
    variables: { first: 300, groupName },
  });
  const pageInfo =
    data === undefined ? undefined : data.group.toeInputs.pageInfo;
  const toeInputsEdges: IToeInputEdge[] =
    data === undefined ? [] : data.group.toeInputs.edges;

  const toeInputs: IToeInputData[] = toeInputsEdges.map(
    ({ node }): IToeInputData => ({
      ...node,
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

  const filterSearchtextResult: IToeInputData[] = filterSearchText(
    toeInputs,
    searchTextFilter
  );
  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const initialSort: string = JSON.stringify({
    dataField: "component",
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
          position: "right",
        }}
        dataset={filterSearchtextResult}
        defaultSorted={JSON.parse(
          _.get(sessionStorage, "toeInputsSort", initialSort)
        )}
        exportCsv={true}
        headers={headersToeInputsTable}
        id={"tblToeInputs"}
        isFilterEnabled={isFilterEnabled}
        onColumnToggle={handleChange}
        onUpdateEnableFilter={handleUpdateFilter}
        pageSize={100}
        search={false}
      />
    </React.StrictMode>
  );
};

export { GroupToeInputsView };
