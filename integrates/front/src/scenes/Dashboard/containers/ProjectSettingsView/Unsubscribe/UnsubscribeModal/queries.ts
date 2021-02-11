import type { DocumentNode } from "graphql";
import gql from "graphql-tag";

const UNSUBSCRIBE_FROM_GROUP_MUTATION: DocumentNode = gql`
  mutation UnsubscribeFromGroupMutation($groupName: String!) {
    unsubscribeFromGroup(groupName: $groupName) {
      success
    }
  }
`;

export { UNSUBSCRIBE_FROM_GROUP_MUTATION };
