import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const ENUMERATE_TOE_INPUT: DocumentNode = gql`
  mutation EnumerateToeInput(
    $component: String!
    $entryPoint: String!
    $groupName: String!
    $seenFirstTimeBy: String!
  ) {
    enumerateToeInput(
      component: $component
      entryPoint: $entryPoint
      groupName: $groupName
      seenFirstTimeBy: $seenFirstTimeBy
    ) {
      success
    }
  }
`;

const GET_STAKEHOLDERS: DocumentNode = gql`
  query GetGroupStakeholderRolesQuery($groupName: String!) {
    group(groupName: $groupName) {
      name
      stakeholders {
        email
        role
      }
    }
  }
`;

export { ENUMERATE_TOE_INPUT, GET_STAKEHOLDERS };
