import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_FINDING_RECORDS: DocumentNode = gql`
  query GetFindingRecords($findingId: String!) {
    finding(identifier: $findingId) {
      records
      id
    }
  }
`;
