import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GROUPS_NAME_QUERY: DocumentNode = gql`
  query InternalGroupName {
    internalNames(entity: GROUP) {
      name
    }
  }
`;

const CREATE_GROUP_MUTATION: DocumentNode = gql`
  mutation CreateGroupMutation(
    $description: String!
    $hasMachine: Boolean
    $hasSquad: Boolean
    $language: Language
    $organization: String!
    $groupName: String!
    $subscription: SubscriptionType
  ) {
    createGroup(
      description: $description
      hasMachine: $hasMachine
      hasSquad: $hasSquad
      language: $language
      organization: $organization
      groupName: $groupName
      subscription: $subscription
    ) {
      success
    }
  }
`;

export { CREATE_GROUP_MUTATION, GROUPS_NAME_QUERY };
