/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for the sake of readability
 */

// Third parties imports
import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import _ from "lodash";
import React, { ReactElement } from "react";
import { Col, Row } from "react-bootstrap";
import { RouteComponentProps } from "react-router";

// Local imports
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeader } from "../../../../components/DataTableNext/types";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import styles from "./index.css";
import { GET_BILL } from "./queries";
import { IBillDeveloper, IData } from "./types";

type ForcesViewProps = RouteComponentProps<{ projectName: string }>;

const projectAuthorsView: React.FunctionComponent<ForcesViewProps> = (props: ForcesViewProps): JSX.Element => {

  const now: Date = new Date();
  const thisYear: number = now.getFullYear();
  const thisMonth: number = now.getMonth();
  const dateRange: Date[] = _
    .range(0, 12)
    .map((month: number) => new Date(thisYear, thisMonth - month));

  const [billDate, setBillDate] = React.useState(dateRange[0].toISOString());

  const formatText: ((value: string) => ReactElement<Text>) =
    (value: string): ReactElement<Text> => <text className={styles.wrapped}>{value}</text>;

  const formatCommit: ((value: string) => ReactElement<Text>) =
    (value: string): ReactElement<Text> => <text className={styles.wrapped}>{value.slice(0, 8)}</text>;

  const formatDate: ((date: Date) => string) = (date: Date): string => {
    const month: number = date.getMonth() + 1;
    const monthStr: string = month.toString();

    return `${monthStr.padStart(2, "0")}/${date.getFullYear()}`;
  };

  const handleDateChange: ((event: React.ChangeEvent<HTMLSelectElement>) => void) =
    (event: React.ChangeEvent<HTMLSelectElement>): void => {
      setBillDate(event.target.value);
    };

  const headersAuthorsTable: IHeader[] = [
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
      header: translate.t("group.authors.groups_contributed"),
      width: "20%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "commit",
      formatter: formatCommit,
      header: translate.t("group.authors.commit"),
      width: "10%",
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

  const { projectName } = props.match.params;

  const { data } = useQuery(GET_BILL, {
    onError: (error: ApolloError): void => {
      msgError(translate.t("group_alerts.error_textsad"));
      rollbar.error("An error occurred getting bill data", error);
    },
    variables: { date: billDate, projectName },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  const dataset: IBillDeveloper[] = (data as IData).project.bill.developers;

  return (
    <React.StrictMode>
      <Row>
        <Col xs={10}>
          <p>{translate.t("group.authors.table_advice")}</p>
        </Col>
      </Row>
      <Row>
        <Col xs={2} className={styles.dateCol}>
          <select onChange={handleDateChange} className={styles.selectDate}>
            {dateRange.map((date: Date, index: number): JSX.Element => (
              <option value={date.toISOString()} key={index}>{formatDate(date)}</option>
            ))}
          </select>
        </Col>
      </Row>
      <DataTableNext
        bordered={true}
        dataset={dataset}
        defaultSorted={{ dataField: "actor", order: "asc" }}
        exportCsv={true}
        headers={headersAuthorsTable}
        id="tblAuthorsList"
        pageSize={100}
        remote={false}
        search={true}
        striped={true}
        title=""
      />
    </React.StrictMode>
  );
};

export { projectAuthorsView as ProjectAuthorsView };
