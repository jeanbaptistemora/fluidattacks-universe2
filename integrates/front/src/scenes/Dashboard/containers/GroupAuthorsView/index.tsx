import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import type { ReactElement } from "react";
import React, { useCallback, useState } from "react";
import { useParams } from "react-router-dom";

import { DataTableNext } from "components/DataTableNext";
import { commitFormatter } from "components/DataTableNext/formatters";
import type {
  IFilterProps,
  IHeaderConfig,
} from "components/DataTableNext/types";
import { filterSearchText, filterText } from "components/DataTableNext/utils";
import styles from "scenes/Dashboard/containers/GroupAuthorsView/index.css";
import { GET_BILL } from "scenes/Dashboard/containers/GroupAuthorsView/queries";
import type {
  IBillAuthor,
  IData,
} from "scenes/Dashboard/containers/GroupAuthorsView/types";
import { Col100, Row } from "styles/styledComponents";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IFilterSet {
  author: string;
  groupsContributed: string;
  repository: string;
}

const GroupAuthorsView: React.FC = (): JSX.Element => {
  const now: Date = new Date();
  const thisYear: number = now.getFullYear();
  const thisMonth: number = now.getMonth();
  const DATE_RANGE = 12;
  const dateRange: Date[] = _.range(0, DATE_RANGE).map(
    (month: number): Date => new Date(thisYear, thisMonth - month)
  );

  const [billDate, setBillDate] = useState(dateRange[0].toISOString());

  const [isCustomFilterEnabled, setCustomFilterEnabled] =
    useStoredState<boolean>("groupAuthorsFilters", false);

  const [searchTextFilter, setSearchTextFilter] = useState("");
  const [filterAuthorsTable, setFilterAuthorsTable] =
    useStoredState<IFilterSet>(
      "filterGroupAuthorsSet",
      {
        author: "",
        groupsContributed: "",
        repository: "",
      },
      localStorage
    );

  const handleUpdateCustomFilter: () => void = useCallback((): void => {
    setCustomFilterEnabled(!isCustomFilterEnabled);
  }, [isCustomFilterEnabled, setCustomFilterEnabled]);

  const formatText: (value: string) => ReactElement<Text> = (
    value: string
  ): ReactElement<Text> => <p className={styles.wrapped}>{value}</p>;

  const formatCommit: (value: string) => ReactElement<Text> = (
    value: string
  ): ReactElement<Text> => (
    <p className={styles.wrapped}>{commitFormatter(value)}</p>
  );

  const formatDate: (date: Date) => string = (date: Date): string => {
    const month: number = date.getMonth() + 1;
    const monthStr: string = month.toString();

    return `${monthStr.padStart(2, "0")}/${date.getFullYear()}`;
  };

  const handleDateChange: (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => void = useCallback(
    (event: React.ChangeEvent<HTMLSelectElement>): void => {
      setBillDate(event.target.value);
    },
    []
  );

  const headersAuthorsTable: IHeaderConfig[] = [
    {
      align: "center",
      dataField: "actor",
      formatter: formatText,
      header: translate.t("group.authors.actor"),
      width: "40%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "groups",
      formatter: formatText,
      header: translate.t("group.authors.groupsContributed"),
      width: "20%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "commit",
      formatter: formatCommit,
      header: translate.t("group.authors.commit"),
      width: "20%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "repository",
      formatter: formatText,
      header: translate.t("group.authors.repository"),
      width: "20%",
      wrapped: true,
    },
  ];

  const { groupName } = useParams<{ groupName: string }>();

  const { data } = useQuery(GET_BILL, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred getting bill data", error);
      });
    },
    variables: { date: billDate, groupName },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const dataset: IBillAuthor[] = (data as IData).group.bill.authors;

  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }
  const filterSearchtextDataset: IBillAuthor[] = filterSearchText(
    dataset,
    searchTextFilter
  );

  function onAuthorChange(event: React.ChangeEvent<HTMLInputElement>): void {
    event.persist();
    setFilterAuthorsTable(
      (value): IFilterSet => ({
        ...value,
        author: event.target.value,
      })
    );
  }
  const filterAuthorDataset: IBillAuthor[] = filterText(
    dataset,
    filterAuthorsTable.author,
    "actor"
  );
  function onGroupsContributedChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    event.persist();
    setFilterAuthorsTable(
      (value): IFilterSet => ({
        ...value,
        groupsContributed: event.target.value,
      })
    );
  }
  const filterGroupsContributedDataset: IBillAuthor[] = filterText(
    dataset,
    filterAuthorsTable.groupsContributed,
    "groups"
  );
  function onRepositoryChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    event.persist();
    setFilterAuthorsTable(
      (value): IFilterSet => ({
        ...value,
        repository: event.target.value,
      })
    );
  }
  const filterRepositoryDataset: IBillAuthor[] = filterText(
    dataset,
    filterAuthorsTable.repository,
    "repository"
  );

  function clearFilters(): void {
    setFilterAuthorsTable(
      (): IFilterSet => ({
        author: "",
        groupsContributed: "",
        repository: "",
      })
    );
    setSearchTextFilter("");
  }

  const resultDataset: IBillAuthor[] = _.intersection(
    filterSearchtextDataset,
    filterAuthorDataset,
    filterRepositoryDataset,
    filterGroupsContributedDataset
  );

  const customFiltersProps: IFilterProps[] = [
    {
      defaultValue: filterAuthorsTable.author,
      onChangeInput: onAuthorChange,
      placeholder: "Author",
      tooltipId: "group.authors.filtersTooltips.actor.id",
      tooltipMessage: "group.authors.filtersTooltips.actor",
      type: "text",
    },
    {
      defaultValue: filterAuthorsTable.groupsContributed,
      onChangeInput: onGroupsContributedChange,
      placeholder: "Groups Contributed",
      tooltipId: "group.authors.filtersTooltips.groupsContributed.id",
      tooltipMessage: "group.authors.filtersTooltips.groupsContributed",
      type: "text",
    },
    {
      defaultValue: filterAuthorsTable.repository,
      onChangeInput: onRepositoryChange,
      placeholder: "Repository",
      tooltipId: "group.authors.filtersTooltips.repository.id",
      tooltipMessage: "group.authors.filtersTooltips.repository",
      type: "text",
    },
  ];

  return (
    <React.StrictMode>
      <Row>
        {/* eslint-disable-next-line react/forbid-component-props */}
        <Col100 className={"pl0"}>
          <p>{translate.t("group.authors.tableAdvice")}</p>
        </Col100>
      </Row>
      <Row>
        {/* eslint-disable-next-line react/forbid-component-props */}
        <Col100 className={styles.dateCol}>
          <select className={styles.selectDate} onChange={handleDateChange}>
            {dateRange.map(
              (date: Date, index: number): JSX.Element => (
                <option
                  key={index.toString()}
                  selected={date.toISOString() === billDate}
                  value={date.toISOString()}
                >
                  {formatDate(date)}
                </option>
              )
            )}
          </select>
        </Col100>
      </Row>
      <DataTableNext
        bordered={true}
        clearFiltersButton={clearFilters}
        customFilters={{
          customFiltersProps,
          isCustomFilterEnabled,
          onUpdateEnableCustomFilter: handleUpdateCustomFilter,
          oneRowMessage: true,
          resultSize: {
            current: resultDataset.length,
            total: dataset.length,
          },
        }}
        customSearch={{
          customSearchDefault: searchTextFilter,
          isCustomSearchEnabled: true,
          onUpdateCustomSearch: onSearchTextChange,
          position: "right",
        }}
        dataset={resultDataset}
        defaultSorted={{ dataField: "actor", order: "asc" }}
        exportCsv={true}
        headers={headersAuthorsTable}
        id={"tblAuthorsList"}
        pageSize={100}
        search={false}
        striped={true}
      />
    </React.StrictMode>
  );
};

export { GroupAuthorsView };
