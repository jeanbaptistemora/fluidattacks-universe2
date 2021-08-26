import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import type { ReactElement } from "react";
import React, { useCallback, useState } from "react";
import type { TableColumnFilterProps } from "react-bootstrap-table-next";
import { textFilter } from "react-bootstrap-table2-filter";
import { useParams } from "react-router-dom";

import { DataTableNext } from "components/DataTableNext";
import { commitFormatter } from "components/DataTableNext/formatters";
import type { IHeaderConfig } from "components/DataTableNext/types";
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

const GroupAuthorsView: React.FC = (): JSX.Element => {
  const now: Date = new Date();
  const thisYear: number = now.getFullYear();
  const thisMonth: number = now.getMonth();
  const DATE_RANGE = 12;
  const dateRange: Date[] = _.range(0, DATE_RANGE).map(
    (month: number): Date => new Date(thisYear, thisMonth - month)
  );

  const [billDate, setBillDate] = useState(dateRange[0].toISOString());

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

  const [isFilterEnabled, setFilterEnabled] = useStoredState<boolean>(
    "groupAuthorsFilters",
    false
  );

  const handleUpdateFilter: () => void = useCallback((): void => {
    setFilterEnabled(!isFilterEnabled);
  }, [isFilterEnabled, setFilterEnabled]);

  const onFilterGroupsContributed: TableColumnFilterProps["onFilter"] = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("groupsContributedFilter", filterVal);
  };
  const onFilterRepository: TableColumnFilterProps["onFilter"] = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("repositoryFilter", filterVal);
  };

  const headersAuthorsTable: IHeaderConfig[] = [
    {
      align: "center",
      dataField: "actor",
      filter: textFilter({
        delay: 1000,
      }),
      formatter: formatText,
      header: translate.t("group.authors.actor"),
      width: "40%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "groups",
      filter: textFilter({
        defaultValue: _.get(sessionStorage, "groupsContributedFilter"),
        delay: 1000,
        onFilter: onFilterGroupsContributed,
      }),
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
      filter: textFilter({
        defaultValue: _.get(sessionStorage, "repositoryFilter"),
        delay: 1000,
        onFilter: onFilterRepository,
      }),
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
        dataset={dataset}
        defaultSorted={{ dataField: "actor", order: "asc" }}
        exportCsv={true}
        headers={headersAuthorsTable}
        id={"tblAuthorsList"}
        isFilterEnabled={isFilterEnabled}
        onUpdateEnableFilter={handleUpdateFilter}
        pageSize={100}
        search={true}
        striped={true}
      />
    </React.StrictMode>
  );
};

export { GroupAuthorsView };
