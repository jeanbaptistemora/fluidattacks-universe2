import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import moment from "moment";
import React, { useCallback } from "react";
import { dateFilter } from "react-bootstrap-table2-filter";
import { useParams } from "react-router-dom";

import { DataTableNext } from "components/DataTableNext";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { GET_TOE_LINES } from "scenes/Dashboard/containers/GroupToeLinesView/queries";
import type {
  IGitRootAttr,
  IToeLinesAttr,
  IToeLinesData,
} from "scenes/Dashboard/containers/GroupToeLinesView/types";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { translate } from "utils/translations/translate";

const GroupToeLinesView: React.FC = (): JSX.Element => {
  const { projectName: groupName } = useParams<{ projectName: string }>();

  const [isFilterEnabled, setFilterEnabled] = useStoredState<boolean>(
    "toeLinesFilters",
    false
  );
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
    const newSorted: Sorted = { dataField, order };
    sessionStorage.setItem("toeLinesSort", JSON.stringify(newSorted));
  };

  const headersToeLinesTable: IHeaderConfig[] = [
    {
      align: "left",
      dataField: "filename",
      header: translate.t("group.toe.lines.filename"),
      onSort,
      width: "40%",
    },
    {
      align: "center",
      dataField: "attacked",
      header: translate.t("group.toe.lines.attacked"),
      onSort,
      width: "2.5%",
    },
    {
      align: "center",
      dataField: "coverage",
      formatter: formatPercentage,
      header: translate.t("group.toe.lines.coverage"),
      onSort,
      width: "2.5%",
    },
    {
      align: "center",
      dataField: "loc",
      header: translate.t("group.toe.lines.loc"),
      onSort,
      width: "10%",
    },
    {
      align: "center",
      dataField: "testedLines",
      header: translate.t("group.toe.lines.testedLines"),
      onSort,
      width: "10%",
    },
    {
      align: "center",
      dataField: "pendingLines",
      header: translate.t("group.toe.lines.pendingLines"),
      onSort,
      width: "5%",
    },
    {
      align: "center",
      dataField: "modifiedDate",
      filter: dateFilter(),
      formatter: formatDate,
      header: translate.t("group.toe.lines.modifiedDate"),
      onSort,
      width: "5%",
    },
    {
      align: "center",
      dataField: "modifiedCommit",
      header: translate.t("group.toe.lines.modifiedCommit"),
      onSort,
      width: "10%",
    },
    {
      align: "center",
      dataField: "testedDate",
      filter: dateFilter(),
      formatter: formatDate,
      header: translate.t("group.toe.lines.testedDate"),
      onSort,
      width: "5%",
    },
    {
      align: "left",
      dataField: "comments",
      header: translate.t("group.toe.lines.comments"),
      onSort,
      width: "15%",
    },
  ];

  // // GraphQL operations
  const { data } = useQuery<{ group: { roots: IGitRootAttr[] } }>(
    GET_TOE_LINES,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          Logger.error("Couldn't load roots", error);
        });
      },
      variables: { groupName },
    }
  );

  const roots: IGitRootAttr[] = data === undefined ? [] : data.group.roots;

  const getAttacked = (toeLinesAttr: IToeLinesAttr): string =>
    toeLinesAttr.testedLines === toeLinesAttr.loc
      ? translate.t("group.toe.lines.yes")
      : translate.t("group.toe.lines.no");
  const getCoverage = (toeLinesAttr: IToeLinesAttr): number =>
    toeLinesAttr.testedLines / toeLinesAttr.loc;
  const getPendingLines = (toeLinesAttr: IToeLinesAttr): number =>
    toeLinesAttr.loc - toeLinesAttr.testedLines;
  const toeLines: IToeLinesData[] = roots.reduce(
    (acc: IToeLinesData[], root: IGitRootAttr): IToeLinesData[] =>
      acc.concat(
        root.toeLines.map(
          (toeLinesAttr: IToeLinesAttr): IToeLinesData => ({
            attacked: getAttacked(toeLinesAttr),
            coverage: getCoverage(toeLinesAttr),
            groupName,
            pendingLines: getPendingLines(toeLinesAttr),
            rootId: root.id,
            ...toeLinesAttr,
          })
        )
      ),
    []
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
        dataset={toeLines}
        defaultSorted={JSON.parse(
          _.get(sessionStorage, "toeLinesSort", initialSort)
        )}
        exportCsv={true}
        headers={headersToeLinesTable}
        id={"tblToeLines"}
        isFilterEnabled={isFilterEnabled}
        onUpdateEnableFilter={handleUpdateFilter}
        pageSize={100}
        search={true}
      />
    </React.StrictMode>
  );
};

export { GroupToeLinesView };
