import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_PROJECT_COMMENTS: DocumentNode = gql`
  query GetProjectComments($projectName: String!) {
    project(projectName: $projectName) {
      comments {
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
    $content: String!, $projectName: String!, $parent: String!
  ) {
    addProjectComment(content: $content, projectName: $projectName, parent: $parent) {
      commentId
      success
    }
  }
`;
