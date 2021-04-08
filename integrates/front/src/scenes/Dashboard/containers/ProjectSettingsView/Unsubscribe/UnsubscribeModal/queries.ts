import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const UNSUBSCRIBE_FROM_GROUP_MUTATION: DocumentNode = gql`
  mutation UnsubscribeFromGroupMutation($groupName: String!) {
    unsubscribeFromGroup(groupName: $groupName) {
      success
    }
  }
`;

export { UNSUBSCRIBE_FROM_GROUP_MUTATION };
