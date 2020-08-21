import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_PROJECT_CONSULTING: DocumentNode = gql`
  query GetProjectConsulting($projectName: String!) {
    project(projectName: $projectName) {
      consulting {
        id
        content
        created
        email
        fullname
        modified
        parent
      }
      name
    }
  }
`;

export const ADD_PROJECT_CONSULT: DocumentNode = gql`
  mutation AddProjectConsult(
    $content: String!, $projectName: String!, $parent: GenericScalar!
  ) {
    addProjectConsult(content: $content, projectName: $projectName, parent: $parent) {
      commentId
      success
    }
  }
`;
