import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const REQUEST_GROUPS_UPGRADE_MUTATION: DocumentNode = gql`
  mutation RequestGroupsUpgrade($groupNames: [String!]!) {
    requestGroupsUpgrade(groupNames: $groupNames) {
      success
    }
  }
`;

export { REQUEST_GROUPS_UPGRADE_MUTATION };
