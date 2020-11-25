import type { DocumentNode } from "graphql";
import gql from "graphql-tag";

const REMOVE_GROUP_MUTATION: DocumentNode = gql`
  mutation RemoveGroupMutation($groupName: String!) {
    removeGroup(groupName: $groupName) {
      success
    }
  }
`;

export { REMOVE_GROUP_MUTATION };
