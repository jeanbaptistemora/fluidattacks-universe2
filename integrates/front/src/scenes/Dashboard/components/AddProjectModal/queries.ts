import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const PROJECTS_NAME_QUERY: DocumentNode = gql`
  query InternalGroupName {
    internalNames(entity: GROUP) {
      name
    }
  }
`;

const CREATE_PROJECT_MUTATION: DocumentNode = gql`
  mutation CreateProjectMutation(
    $description: String!
    $hasDrills: Boolean
    $hasForces: Boolean
    $language: Language
    $organization: String!
    $projectName: String!
    $subscription: SubscriptionType
  ) {
    createProject(
      description: $description
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

export { CREATE_PROJECT_MUTATION, PROJECTS_NAME_QUERY };
