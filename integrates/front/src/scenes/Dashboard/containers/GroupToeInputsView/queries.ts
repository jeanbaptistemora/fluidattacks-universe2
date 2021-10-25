import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_TOE_INPUTS: DocumentNode = gql`
  query GetToeInputs($groupName: String!) {
    group(groupName: $groupName) {
      name
      toeInputs {
        component
        createdDate
        entryPoint
        seenFirstTimeBy
        testedDate
        unreliableRootNickname
      }
    }
  }
`;

export { GET_TOE_INPUTS };
