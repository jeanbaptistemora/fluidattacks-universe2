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
  query GetRootsInfo($groupName: String!) {
    group(groupName: $groupName) {
      name
      roots {
        ... on GitRoot {
          __typename
          environmentUrls
          gitEnvironmentUrls {
            url
            id
            urlType
          }
          id
          nickname
          state
        }
        ... on IPRoot {
          __typename
          id
          nickname
        }
        ... on URLRoot {
          __typename
          host
          id
          nickname
          path
          port
          protocol
          query
          state
        }
      }
    }
  }
`;

export { ADD_TOE_INPUT, GET_ROOTS };
