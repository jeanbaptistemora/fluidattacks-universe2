import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_DOCUMENT: DocumentNode = gql`
  query AnalyticsQuery(
    $groupName: String!
    $riskOverTimeDocumentName: String!
    $riskOverTimeDocumentType: String!
    $whereToFindingsDocumentName: String!
    $whereToFindingsDocumentType: String!
  ) {
    riskOverTime: analytics {
      document: groupDocument(
        documentName: $riskOverTimeDocumentName
        documentType: $riskOverTimeDocumentType
        groupName: $groupName
      )
    }
    whereToFindings: analytics {
      document: groupDocument(
        documentName: $whereToFindingsDocumentName
        documentType: $whereToFindingsDocumentType
        groupName: $groupName
      )
    }
  }
  `;
