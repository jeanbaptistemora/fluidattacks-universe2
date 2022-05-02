import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_VERIFIED_FINDING_INFO: DocumentNode = gql`
  query GetVerifiedFindingInfo($groupName: String!) {
    group(groupName: $groupName) {
      findings {
        id
        title
        verified
      }
      name
    }
  }
`;

export { GET_VERIFIED_FINDING_INFO };
