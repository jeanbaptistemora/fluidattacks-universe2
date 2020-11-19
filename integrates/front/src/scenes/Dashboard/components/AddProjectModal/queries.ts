import type { DocumentNode } from "graphql";
import gql from "graphql-tag";

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
    $organization: String!
    $projectName: String!
    $subscription: SubscriptionType
  ) {
    createProject(
      description: $description
      hasDrills: $hasDrills
      hasForces: $hasForces
      organization: $organization
      projectName: $projectName
      subscription: $subscription
    ) {
      success
    }
  }
`;

export { CREATE_PROJECT_MUTATION, PROJECTS_NAME_QUERY };
