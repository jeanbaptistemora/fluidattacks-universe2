import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const ADD_TOE_PORT: DocumentNode = gql`
  mutation AddToePort(
    $address: String!
    $groupName: String!
    $port: Int!
    $rootId: String!
  ) {
    addToePort(
      address: $address
      groupName: $groupName
      port: $port
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
        }
        ... on IPRoot {
          __typename
          address
          id
          nickname
          state
        }
        ... on URLRoot {
          __typename
        }
      }
    }
  }
`;

export { ADD_TOE_PORT, GET_ROOTS };
