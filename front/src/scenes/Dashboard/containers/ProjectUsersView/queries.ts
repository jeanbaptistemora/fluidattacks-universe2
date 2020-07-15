import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_USERS: DocumentNode = gql`
  query GetUsersQuery($projectName: String!) {
    project(projectName: $projectName){
      users {
        email
        role
        responsibility
        phoneNumber
        firstLogin
        lastLogin
      }
    }
  }
  `;

export const REMOVE_USER_MUTATION: DocumentNode = gql`
  mutation RemoveUserAccessMutation($projectName: String!, $userEmail: String!, ) {
    removeUserAccess (
      projectName: $projectName
      userEmail: $userEmail
    ) {
      removedEmail
      success
    }
  }
  `;

export const ADD_USER_MUTATION: DocumentNode = gql`
  mutation GrantUserMutation(
    $email: String!,
    $phoneNumber: String,
    $projectName: String,
    $responsibility: String,
    $role: UserRole!
    ) {
    grantUserAccess (
      email: $email,
      phoneNumber: $phoneNumber,
      projectName: $projectName,
      responsibility: $responsibility,
      role: $role) {
      success
      grantedUser {
        email
        role
        responsibility
        phoneNumber
        firstLogin
        lastLogin
      }
    }
  }
  `;

export const EDIT_USER_MUTATION: DocumentNode = gql`
  mutation EditUserMutation(
    $email: String!,
    $phoneNumber: String!,
    $projectName: String!,
    $responsibility: String!,
    $role: UserRole!
    ) {
    editUser (
      email: $email,
      phoneNumber: $phoneNumber,
      projectName: $projectName,
      responsibility: $responsibility,
      role: $role) {
      success
    }
  }
  `;
