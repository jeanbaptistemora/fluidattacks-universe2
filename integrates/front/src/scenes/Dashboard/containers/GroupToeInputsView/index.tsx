import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import moment from "moment";
import React, { useCallback } from "react";
import type { SortOrder } from "react-bootstrap-table-next";
import { dateFilter } from "react-bootstrap-table2-filter";
import { useParams } from "react-router-dom";

import { DataTableNext } from "components/DataTableNext";
import { commitFormatter } from "components/DataTableNext/formatters";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { GET_TOE_INPUTS } from "scenes/Dashboard/containers/GroupToeInputsView/queries";
import type {
  IToeInputAttr,
  IToeInputData,
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
      commit: true,
      component: true,
      createdDate: true,
      entryPoint: true,
      seenFirstTimeBy: true,
      testedDate: true,
      unreliableRootNickname: true,
      verified: true,
      vulnerabilities: true,
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
    "toeInputsFilters",
    false
  );
  const handleUpdateFilter: () => void = useCallback((): void => {
    setFilterEnabled(!isFilterEnabled);
  }, [isFilterEnabled, setFilterEnabled]);

  const formatDate: (date: string) => string = (date: string): string => {
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
      dataField: "verified",
      header: translate.t("group.toe.inputs.verified"),
      onSort,
      visible: checkedItems.verified,
      width: "2.5%",
    },
    {
      align: "center",
      dataField: "commit",
      header: translate.t("group.toe.inputs.commit"),
      onSort,
      visible: checkedItems.commit,
      width: "15%",
    },
    {
      align: "center",
      dataField: "testedDate",
      filter: dateFilter({}),
      formatter: formatDate,
      header: translate.t("group.toe.inputs.testedDate"),
      onSort,
      visible: checkedItems.testedDate,
      width: "8%",
    },
    {
      align: "left",
      dataField: "vulnerabilities",
      header: translate.t("group.toe.inputs.vulns"),
      onSort,
      visible: checkedItems.vulnerabilities,
      width: "15%",
    },
    {
      align: "center",
      dataField: "createdDate",
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
  const { data } = useQuery<{ group: { toeInputs: IToeInputAttr[] } }>(
    GET_TOE_INPUTS,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          Logger.error("Couldn't load toe inputs", error);
        });
      },
      variables: { groupName },
    }
  );

  const toeInputs: IToeInputData[] =
    data === undefined
      ? []
      : data.group.toeInputs.map(
          (toeInput: IToeInputData): IToeInputData => ({
            ...toeInput,
            commit: commitFormatter(toeInput.commit),
          })
        );

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
        dataset={toeInputs}
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
        search={true}
      />
    </React.StrictMode>
  );
};

export { GroupToeInputsView };
