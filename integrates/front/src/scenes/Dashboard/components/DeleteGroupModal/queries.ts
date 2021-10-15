import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const REMOVE_GROUP_MUTATION: DocumentNode = gql`
  mutation RemoveGroupMutation(
    $groupName: String!
    $reason: RemoveGroupReason!
  ) {
    removeGroup(groupName: $groupName, reason: $reason) {
      success
    }
  }
`;

export { REMOVE_GROUP_MUTATION };
