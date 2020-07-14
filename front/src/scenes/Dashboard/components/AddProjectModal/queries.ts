import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const PROJECTS_NAME_QUERY: DocumentNode = gql`
  query InternalProjectName {
    internalProjectNames{
      projectName
    }
  }
`;

export const CREATE_PROJECT_MUTATION: DocumentNode = gql`
  mutation CreateProjectMutation(
    $company: String!
    $description: String!,
    $hasDrills: Boolean,
    $hasForces: Boolean,
    $projectName: String!,
    $subscription: SubscriptionType,
    ) {
    createProject(
      company: $company,
      description: $description,
      hasDrills: $hasDrills,
      hasForces: $hasForces,
      projectName: $projectName,
      subscription: $subscription,
    ) {
      success
    }
  }
`;
