import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_PROJECT_COMMENTS: DocumentNode = gql`
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

export const ADD_PROJECT_COMMENT: DocumentNode = gql`
  mutation AddProjectComment(
    $content: String!, $projectName: String!, $parent: GenericScalar!
  ) {
    addProjectComment(content: $content, projectName: $projectName, parent: $parent) {
      commentId
      success
    }
  }
`;
