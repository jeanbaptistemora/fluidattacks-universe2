import type { ApolloError } from "apollo-client";
import { DataTableNext } from "components/DataTableNext";
import { GET_BILL } from "scenes/Dashboard/containers/ProjectAuthorsView/queries";
import type { GraphQLError } from "graphql";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { Logger } from "utils/logger";
import React from "react";
import type { ReactElement } from "react";
import _ from "lodash";
import { msgError } from "utils/notifications";
import styles from "scenes/Dashboard/containers/ProjectAuthorsView/index.css";
import { translate } from "utils/translations/translate";
import { useParams } from "react-router";
import { useQuery } from "@apollo/react-hooks";
import { Col100, Row } from "styles/styledComponents";
import type {
  IBillDeveloper,
  IData,
} from "scenes/Dashboard/containers/ProjectAuthorsView/types";

const ProjectAuthorsView: React.FC = (): JSX.Element => {
  const now: Date = new Date();
  const thisYear: number = now.getFullYear();
  const thisMonth: number = now.getMonth();
  const DATE_RANGE = 12;
  const dateRange: Date[] = _.range(0, DATE_RANGE).map(
    (month: number): Date => new Date(thisYear, thisMonth - month)
  );

  const [billDate, setBillDate] = React.useState(dateRange[0].toISOString());

  const formatText: (value: string) => ReactElement<Text> = (
    value: string
  ): ReactElement<Text> => <p className={styles.wrapped}>{value}</p>;

  const COMMIT_LENGTH = 8;
  const formatCommit: (value: string) => ReactElement<Text> = (
    value: string
  ): ReactElement<Text> => (
    <p className={styles.wrapped}>{value.slice(0, COMMIT_LENGTH)}</p>
  );

  const formatDate: (date: Date) => string = (date: Date): string => {
    const month: number = date.getMonth() + 1;
    const monthStr: string = month.toString();

    return `${monthStr.padStart(2, "0")}/${date.getFullYear()}`;
  };

  const handleDateChange: (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => void = React.useCallback(
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

  const { projectName } = useParams<{ projectName: string }>();

  const { data } = useQuery(GET_BILL, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred getting bill data", error);
      });
    },
    variables: { date: billDate, projectName },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const dataset: IBillDeveloper[] = (data as IData).project.bill.developers;

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
                <option key={index.toString()} value={date.toISOString()}>
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
        pageSize={100}
        search={true}
        striped={true}
      />
    </React.StrictMode>
  );
};

export { ProjectAuthorsView };
