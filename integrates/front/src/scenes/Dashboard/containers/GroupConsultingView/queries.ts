import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_GROUP_CONSULTING: DocumentNode = gql`
  query GetProjectConsulting($projectName: String!) {
    group(projectName: $projectName) {
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

const ADD_PROJECT_CONSULT: DocumentNode = gql`
  mutation AddProjectConsult(
    $content: String!
    $projectName: String!
    $parent: GenericScalar!
  ) {
    addProjectConsult(
      content: $content
      projectName: $projectName
      parent: $parent
    ) {
      commentId
      success
    }
  }
`;

export { ADD_PROJECT_CONSULT, GET_GROUP_CONSULTING };
