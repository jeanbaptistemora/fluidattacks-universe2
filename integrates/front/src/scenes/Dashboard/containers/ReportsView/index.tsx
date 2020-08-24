import { useLazyQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import React from "react";
import { Button, Col, Row } from "react-bootstrap";
import { Logger } from "../../../../utils/logger";
import { msgError } from "../../../../utils/notifications";
import { openUrl } from "../../../../utils/resourceHelpers";
import { translate } from "../../../../utils/translations/translate";
import { default as style } from "./index.css";
import { GET_COMPLETE_REPORT } from "./queries";

const reportsView: React.FC = (): JSX.Element => {
  const { userEmail } = window as typeof window & Dictionary<string>;
  const [getCompleteReport, { data: completeReportData }] = useLazyQuery(GET_COMPLETE_REPORT, {
    fetchPolicy: "network-only",
    onCompleted: (): void => {
      openUrl(completeReportData.report.url);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning(
          "An error occurred downloading the complete report",
          error,
        );
      });
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
