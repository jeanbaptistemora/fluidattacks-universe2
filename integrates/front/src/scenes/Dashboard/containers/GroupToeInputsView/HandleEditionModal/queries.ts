import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const UPDATE_TOE_INPUT: DocumentNode = gql`
  mutation UpdateToeInput(
    $bePresent: Boolean!
    $component: String!
    $entryPoint: String!
    $groupName: String!
    $hasRecentAttack: Boolean
  ) {
    updateToeInput(
      bePresent: $bePresent
      component: $component
      entryPoint: $entryPoint
      groupName: $groupName
      hasRecentAttack: $hasRecentAttack
    ) {
      success
    }
  }
`;

export { UPDATE_TOE_INPUT };
