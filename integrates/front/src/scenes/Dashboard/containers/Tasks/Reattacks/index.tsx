import { useQuery } from "@apollo/client";
import _ from "lodash";
import React, { useState } from "react";
import type { SortOrder } from "react-bootstrap-table-next";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";

import { Table } from "components/Table";
import { tooltipFormatter } from "components/Table/headerFormatters/tooltipFormatter";
import type { IHeaderConfig } from "components/Table/types";
import { filterSearchText } from "components/Table/utils";
import { formatState } from "scenes/Dashboard/containers/GroupFindingsView/utils";
import { GET_TODO_REATTACKS } from "scenes/Dashboard/containers/Tasks/Reattacks/queries";
import type {
  IFindingFormatted,
  IGetTodoReattacks,
  ITodoFindingToReattackAttr,
  ITodoGroupAttr,
  ITodoOrganizationAttr,
} from "scenes/Dashboard/containers/Tasks/Reattacks/types";
import { formatFindings } from "scenes/Dashboard/containers/Tasks/Reattacks/utils";
import { Logger } from "utils/logger";

export const TasksReattacks: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { push } = useHistory();
  const [searchTextFilter, setSearchTextFilter] = useState("");

  const onSortState: (dataField: string, order: SortOrder) => void = (
    dataField: string,
    order: SortOrder
  ): void => {
    const newSorted = { dataField, order };
    sessionStorage.setItem("todoReattackSort", JSON.stringify(newSorted));
  };

  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "title",
      header: "Type",
      onSort: onSortState,
      width: "30%",
      wrapped: true,
    },
    {
      dataField: "age",
      header: "Age",
      onSort: onSortState,
      width: "10%",
      wrapped: true,
    },
    {
      dataField: "lastVulnerability",
      formatter: (value: number): string =>
        t("group.findings.description.value", { count: value }),
      header: "Last Report",
      onSort: onSortState,
      width: "10%",
      wrapped: true,
    },
    {
      dataField: "state",
      formatter: formatState,
      header: "Status",
      onSort: onSortState,
      width: "10%",
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
      header: "Open Vulnerabilities",
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
      dataField: "oldestReattackRequestedDate",
      header: "Reattack Date",
      headerFormatter: tooltipFormatter,
      onSort: onSortState,
      tooltipDataField: "Oldest Requested Reattack Date",
      width: "10%",
    },
  ];

  const { data } = useQuery<IGetTodoReattacks>(GET_TODO_REATTACKS, {
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        Logger.warning(
          "An error occurred fetching user findings from dashboard",
          error
        );
      });
    },
  });

  const dataset: IFindingFormatted[] = formatFindings(
    _.isUndefined(data) || _.isEmpty(data)
      ? []
      : _.flatten(
          data.me.organizations.map(
            (org: ITodoOrganizationAttr): ITodoFindingToReattackAttr[] =>
              org.name === "imamura"
                ? []
                : _.flatten(
                    org.groups.map(
                      (group: ITodoGroupAttr): ITodoFindingToReattackAttr[] =>
                        group.findings
                    )
                  )
          )
        )
  );

  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }
  const filterSearchTextResult: ITodoFindingToReattackAttr[] = filterSearchText(
    dataset,
    searchTextFilter
  );

  const goToFinding: (
    event: React.FormEvent<HTMLButtonElement>,
    rowInfo: { id: string }
  ) => void = (
    _0: React.FormEvent<HTMLButtonElement>,
    rowInfo: { id: string }
  ): void => {
    const [findingSelected]: ITodoFindingToReattackAttr[] = dataset.filter(
      (findingAttr: ITodoFindingToReattackAttr): boolean =>
        findingAttr.id === rowInfo.id
    );
    push(`/groups/${findingSelected.groupName}/vulns/${rowInfo.id}/locations`);
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
        id={"tblTodoReattacks"}
        pageSize={25}
        rowEvents={{ onClick: goToFinding }}
        search={false}
      />
    </React.StrictMode>
  );
};
