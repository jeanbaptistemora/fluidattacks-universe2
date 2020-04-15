import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const ADD_USER_MUTATION: DocumentNode = gql`
  mutation AddUserMutation(
    $email: String!,
    $organization: String!,
    $role: String!
    $phoneNumber: String,
    ) {
    addUser (
      email: $email,
      organization: $organization,
      role: $role,
      phoneNumber: $phoneNumber,
    ) {
      success
      email
    }
  }
`;

export const GET_BROADCAST_MESSAGES: DocumentNode = gql`
  subscription GetBroadcastMessages {
    broadcast
  }
`;

export const GET_PERMISSIONS: DocumentNode = gql`
  query GetPermissions($projectName: String) {
    me(callerOrigin: "FRONT") {
      permissions(projectName: $projectName)
    }
  }
`;
