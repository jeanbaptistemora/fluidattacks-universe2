import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const UPDATE_TOE_INPUT: DocumentNode = gql`
  mutation UpdateToeInput(
    $attackedAt: DateTime
    $bePresent: Boolean!
    $component: String!
    $entryPoint: String!
    $groupName: String!
  ) {
    updateToeInput(
      attackedAt: $attackedAt
      bePresent: $bePresent
      component: $component
      entryPoint: $entryPoint
      groupName: $groupName
    ) {
      success
    }
  }
`;

export { UPDATE_TOE_INPUT };
