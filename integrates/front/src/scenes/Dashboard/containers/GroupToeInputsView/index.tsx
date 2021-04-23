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
import { GET_TOE_INPUTS } from "scenes/Dashboard/containers/GroupToeInputsView/queries";
import type {
  IToeInputAttr,
  IToeInputData,
} from "scenes/Dashboard/containers/GroupToeInputsView/types";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { translate } from "utils/translations/translate";

const GroupToeInputsView: React.FC = (): JSX.Element => {
  const { projectName: groupName } = useParams<{ projectName: string }>();

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
    const newSorted: Sorted = { dataField, order };
    sessionStorage.setItem("toeInputsSort", JSON.stringify(newSorted));
  };
  const headersToeInputsTable: IHeaderConfig[] = [
    {
      align: "left",
      dataField: "component",
      header: translate.t("group.toe.inputs.component"),
      onSort,
      width: "30%",
    },
    {
      align: "left",
      dataField: "entryPoint",
      header: translate.t("group.toe.inputs.entryPoint"),
      onSort,
      width: "10%",
    },
    {
      align: "center",
      dataField: "verified",
      header: translate.t("group.toe.inputs.verified"),
      onSort,
      width: "5%",
    },
    {
      align: "center",
      dataField: "commit",
      header: translate.t("group.toe.inputs.commit"),
      onSort,
      width: "15%",
    },
    {
      align: "center",
      dataField: "testedDate",
      filter: dateFilter(),
      formatter: formatDate,
      header: translate.t("group.toe.inputs.testedDate"),
      onSort,
      width: "5%",
    },
    {
      align: "left",
      dataField: "vulns",
      header: translate.t("group.toe.inputs.vulns"),
      onSort,
      width: "15%",
    },
    {
      align: "center",
      dataField: "createdDate",
      filter: dateFilter(),
      formatter: formatDate,
      header: translate.t("group.toe.inputs.createdDate"),
      onSort,
      width: "5%",
    },
    {
      align: "left",
      dataField: "seenFirstTimeBy",
      header: translate.t("group.toe.inputs.seenFirstTimeBy"),
      onSort,
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
    data === undefined ? [] : data.group.toeInputs;

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
        onUpdateEnableFilter={handleUpdateFilter}
        pageSize={100}
        search={true}
      />
    </React.StrictMode>
  );
};

export { GroupToeInputsView };
