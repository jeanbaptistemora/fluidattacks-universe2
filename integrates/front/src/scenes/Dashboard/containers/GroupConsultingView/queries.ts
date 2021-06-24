import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_GROUP_CONSULTING: DocumentNode = gql`
  query GetGroupConsulting($groupName: String!) {
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

const ADD_GROUP_CONSULT: DocumentNode = gql`
  mutation addGroupConsult(
    $content: String!
    $groupName: String!
    $parent: GenericScalar!
  ) {
    addGroupConsult(content: $content, groupName: $groupName, parent: $parent) {
      commentId
      success
    }
  }
`;

export { ADD_GROUP_CONSULT, GET_GROUP_CONSULTING };
