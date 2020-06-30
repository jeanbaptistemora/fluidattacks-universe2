import { useLazyQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import React from "react";
import { Button, Col, Row } from "react-bootstrap";
import { RouteComponentProps } from "react-router";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { default as style } from "./index.css";
import { GET_COMPLETE_REPORT } from "./queries";

const reportsView: React.FC<RouteComponentProps> = (props: RouteComponentProps): JSX.Element => {
  const { userEmail } = window as typeof window & Dictionary<string>;
  const [getCompleteReport, { data: completeReportData }] = useLazyQuery(GET_COMPLETE_REPORT, {
    fetchPolicy: "network-only",
    onCompleted: (): void => {
      const newTab: Window | null = window.open(completeReportData.report.url);
      (newTab as Window).opener = undefined;
    },
    onError: (downloadError: ApolloError): void => {
      msgError(translate.t("group_alerts.error_textsad"));
      rollbar.error(
        "An error occurred downloading the complete report",
        downloadError,
      );
    },
  });

  const handleDownloadCompleteReport: (() => void) = (): void => {
    getCompleteReport({ variables: { reportType: "COMPLETE", userEmail } });
  };

  return (
    <React.StrictMode>
      <div className={style.container}>
        <Row>
          <Col md={10} sm={8}>
            <h2>Reports</h2>
            <Button onClick={handleDownloadCompleteReport}>Download</Button>
          </Col>
        </Row>
      </div>
    </React.StrictMode>
  );
};

export { reportsView as ReportsView };
