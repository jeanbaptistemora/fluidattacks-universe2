import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_TOE_INPUTS: DocumentNode = gql`
  query GetToeInputs($groupName: String!) {
    group: project(projectName: $groupName) {
      name
      toeInputs {
        commit
        component
        createdDate
        entryPoint
        seenFirstTimeBy
        testedDate
        verified
        vulns
      }
    }
  }
`;

export { GET_TOE_INPUTS };
