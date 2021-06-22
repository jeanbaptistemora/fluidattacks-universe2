import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FORCES_TOKEN: DocumentNode = gql`
  query ASMGetForcesToken($groupName: String!) {
    group(groupName: $groupName) {
      forcesToken
      name
    }
  }
`;

const UPDATE_FORCES_TOKEN_MUTATION: DocumentNode = gql`
  mutation ASMUpdateForcesAccessTokenMutation($groupName: String!) {
    updateForcesAccessToken(groupName: $groupName) {
      success
      sessionJwt
    }
  }
`;

export { GET_FORCES_TOKEN, UPDATE_FORCES_TOKEN_MUTATION };
