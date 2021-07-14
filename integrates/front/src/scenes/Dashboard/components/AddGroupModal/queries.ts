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
    $groupName: String!
    $hasMachine: Boolean!
    $hasSquad: Boolean!
    $language: Language!
    $organization: String!
    $service: ServiceType!
    $subscription: SubscriptionType!
  ) {
    createGroup(
      description: $description
      groupName: $groupName
      hasMachine: $hasMachine
      hasSquad: $hasSquad
      language: $language
      organization: $organization
      service: $service
      subscription: $subscription
    ) {
      success
    }
  }
`;

export { CREATE_GROUP_MUTATION, GROUPS_NAME_QUERY };
