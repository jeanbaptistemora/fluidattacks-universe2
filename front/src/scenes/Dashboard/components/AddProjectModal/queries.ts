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
    $companies: [String]!
    $description: String!,
    $projectName: String!,
    ) {
    createProject(
      companies: $companies,
      description: $description,
      projectName: $projectName,
    ) {
      success
    }
  }
`;
