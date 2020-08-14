import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_COMPLETE_REPORT: DocumentNode = gql`
  query getCompleteReport($reportType:ReportType!, $userEmail: String!) {
    report(reportType:$reportType, userEmail: $userEmail) {
      url
    }
  }
`;
