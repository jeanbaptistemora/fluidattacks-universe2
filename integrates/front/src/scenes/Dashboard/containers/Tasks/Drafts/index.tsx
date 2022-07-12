import { useQuery } from "@apollo/client";
import _ from "lodash";
import React, { useState } from "react";
import type { SortOrder } from "react-bootstrap-table-next";
import { selectFilter } from "react-bootstrap-table2-filter";
import { useHistory } from "react-router-dom";

import { Table } from "components/Table";
import type { IHeaderConfig } from "components/Table/types";
import { filterSearchText } from "components/Table/utils";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import { GET_TODO_DRAFTS } from "scenes/Dashboard/containers/Tasks/Drafts/queries";
import type {
  IGetTodoDrafts,
  ITodoDraftAttr,
  ITodoGroupAttr,
  ITodoOrganizationAttr,
} from "scenes/Dashboard/containers/Tasks/Drafts/types";
import { Logger } from "utils/logger";

export const TasksDrafts: React.FC = (): JSX.Element => {
  const { push } = useHistory();
  const [searchTextFilter, setSearchTextFilter] = useState("");
  const selectOptionsStatus = {
    CREATED: "Created",
    REJECTED: "Rejected",
    SUBMITTED: "Submitted",
  };

  const onFilterStatus: (filterVal: string) => void = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("todoDraftStatusFilter", filterVal);
  };

  const onSortState: (dataField: string, order: SortOrder) => void = (
    dataField: string,
    order: SortOrder
  ): void => {
    const newSorted = { dataField, order };
    sessionStorage.setItem("todoDraftSort", JSON.stringify(newSorted));
  };

  const hackerFormatter = (value: string): JSX.Element => {
    return <div className={`tl truncate`}>{value}</div>;
  };

  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "reportDate",
      header: "Date",
      onSort: onSortState,
      width: "10%",
    },

    {
      dataField: "title",
      header: "Type",
      onSort: onSortState,
      width: "30%",
      wrapped: true,
    },
    {
      dataField: "severityScore",
      header: "Severity",
      onSort: onSortState,
      width: "10%",
    },
    {
      dataField: "openVulnerabilities",
      header: "Open Vulns.",
      onSort: onSortState,
      width: "10%",
    },
    {
      dataField: "groupName",
      header: "Group Name",
      onSort: onSortState,
      width: "10%",
    },
    {
      dataField: "hacker",
      formatter: hackerFormatter,
      header: "Hacker",
      onSort: onSortState,
      width: "10%",
    },
    {
      dataField: "currentState",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "todoDraftStatusFilter"),
        onFilter: onFilterStatus,
        options: selectOptionsStatus,
      }),
      formatter: statusFormatter,
      header: "State",
      onSort: onSortState,
      width: "10%",
      wrapped: true,
    },
  ];

  const { data } = useQuery<IGetTodoDrafts>(GET_TODO_DRAFTS, {
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        Logger.warning(
          "An error occurred fetching user drafts from dashboard",
          error
        );
      });
    },
  });

  const dataset: ITodoDraftAttr[] =
    _.isUndefined(data) || _.isEmpty(data)
      ? []
      : _.flatten(
          data.me.organizations.map(
            (org: ITodoOrganizationAttr): ITodoDraftAttr[] =>
              org.name === "imamura"
                ? []
                : _.flatten(
                    org.groups.map(
                      (group: ITodoGroupAttr): ITodoDraftAttr[] => group.drafts
                    )
                  )
          )
        );

  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }
  const filterSearchTextResult: ITodoDraftAttr[] = filterSearchText(
    dataset,
    searchTextFilter
  );

  const goToDraft: (
    event: React.FormEvent<HTMLButtonElement>,
    rowInfo: { id: string }
  ) => void = (
    _0: React.FormEvent<HTMLButtonElement>,
    rowInfo: { id: string }
  ): void => {
    const [draftSelected]: ITodoDraftAttr[] = dataset.filter(
      (draftAttr: ITodoDraftAttr): boolean => draftAttr.id === rowInfo.id
    );
    push(`/groups/${draftSelected.groupName}/drafts/${rowInfo.id}/locations`);
  };

  return (
    <React.StrictMode>
      <Table
        customSearch={{
          customSearchDefault: searchTextFilter,
          isCustomSearchEnabled: true,
          onUpdateCustomSearch: onSearchTextChange,
          position: "right",
        }}
        dataset={filterSearchTextResult}
        exportCsv={true}
        headers={tableHeaders}
        id={"tblTodoDrafts"}
        pageSize={25}
        rowEvents={{ onClick: goToDraft }}
        search={false}
      />
    </React.StrictMode>
  );
};
