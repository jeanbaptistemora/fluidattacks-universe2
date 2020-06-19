import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_DOCUMENT: DocumentNode = gql`
  query AnalyticsQuery(
    $documentName: String!
    $documentType: String!
    $groupName: String!
  ) {
    analytics {
      groupDocument(
        documentName: $documentName
        documentType: $documentType
        groupName: $groupName
      )
    }
  }
  `;
