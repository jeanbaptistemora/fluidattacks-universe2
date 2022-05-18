import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_GROUP_FINDINGS: DocumentNode = gql`
  query GetGroupFindings($groupName: String!) {
    group(groupName: $groupName) {
      findings {
        id
        title
      }
      name
    }
  }
`;

export { GET_GROUP_FINDINGS };
