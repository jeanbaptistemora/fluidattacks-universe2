import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_FINDING_RECORDS: DocumentNode = gql`
  query GetFindingRecords($findingId: String!) {
    finding(identifier: $findingId) {
      records
      id
    }
  }
`;
