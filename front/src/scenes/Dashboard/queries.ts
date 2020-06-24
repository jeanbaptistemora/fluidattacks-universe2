import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const ADD_USER_MUTATION: DocumentNode = gql`
  mutation AddUserMutation(
    $email: String!,
    $organization: String!,
    $role: UserRole!
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

export const GET_USER_PERMISSIONS: DocumentNode = gql`
  query GetPermissions($projectName: String) {
    me(callerOrigin: "FRONT") {
      permissions(projectName: $projectName)
      role(projectName: $projectName)
    }
  }
`;
