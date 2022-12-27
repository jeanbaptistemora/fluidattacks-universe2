import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const REMOVE_GROUP_MUTATION: DocumentNode = gql`
  mutation RemoveGroupMutation(
    $comments: String
    $groupName: String!
    $reason: RemoveGroupReason!
  ) {
    removeGroup(comments: $comments, groupName: $groupName, reason: $reason) {
      success
    }
  }
`;

export { REMOVE_GROUP_MUTATION };
