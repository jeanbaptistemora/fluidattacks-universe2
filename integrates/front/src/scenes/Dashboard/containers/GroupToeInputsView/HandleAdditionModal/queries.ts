import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const ADD_TOE_INPUT: DocumentNode = gql`
  mutation AddToeInput(
    $component: String!
    $entryPoint: String!
    $groupName: String!
    $rootId: String!
  ) {
    addToeInput(
      component: $component
      entryPoint: $entryPoint
      groupName: $groupName
      rootId: $rootId
    ) {
      success
    }
  }
`;

const GET_ROOTS: DocumentNode = gql`
  query GetRoots($groupName: String!) {
    group(groupName: $groupName) {
      name
      roots {
        ... on GitRoot {
          environmentUrls
          id
          nickname
          state
        }
        ... on IPRoot {
          address
          id
          nickname
          port
          state
        }
        ... on URLRoot {
          host
          id
          nickname
          path
          port
          protocol
          state
        }
      }
    }
  }
`;

export { ADD_TOE_INPUT, GET_ROOTS };
