import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const REMOVE_GROUP_MUTATION: DocumentNode = gql`
  mutation RemoveGroupMutation($groupName: String!) {
    removeGroup(groupName: $groupName) {
      success
    }
  }
`;

export { REMOVE_GROUP_MUTATION };
