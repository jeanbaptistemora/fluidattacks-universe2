import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_GROUP_CONSULTING: DocumentNode = gql`
  query GetProjectConsulting($groupName: String!) {
    group(groupName: $groupName) {
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
    $groupName: String!
    $parent: GenericScalar!
  ) {
    addProjectConsult(
      content: $content
      projectName: $groupName
      parent: $parent
    ) {
      commentId
      success
    }
  }
`;

export { ADD_PROJECT_CONSULT, GET_GROUP_CONSULTING };
