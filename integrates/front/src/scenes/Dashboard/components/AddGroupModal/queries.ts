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
    $hasSkims: Boolean
    $hasDrills: Boolean
    $hasForces: Boolean
    $language: Language
    $organization: String!
    $projectName: String!
    $subscription: SubscriptionType
  ) {
    createGroup(
      description: $description
      hasSkims: $hasSkims
      hasDrills: $hasDrills
      hasForces: $hasForces
      language: $language
      organization: $organization
      projectName: $projectName
      subscription: $subscription
    ) {
      success
    }
  }
`;

export { CREATE_GROUP_MUTATION, GROUPS_NAME_QUERY };
