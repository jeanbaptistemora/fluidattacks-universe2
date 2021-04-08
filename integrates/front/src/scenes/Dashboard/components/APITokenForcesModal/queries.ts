import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FORCES_TOKEN: DocumentNode = gql`
  query IntegratesGetForcesToken($groupName: String!) {
    project(projectName: $groupName) {
      forcesToken
      name
    }
  }
`;

const UPDATE_FORCES_TOKEN_MUTATION: DocumentNode = gql`
  mutation IntegratesUpdateForcesAccessTokenMutation($groupName: String!) {
    updateForcesAccessToken(projectName: $groupName) {
      success
      sessionJwt
    }
  }
`;

export { GET_FORCES_TOKEN, UPDATE_FORCES_TOKEN_MUTATION };
