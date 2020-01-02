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
        organization
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
  mutation AddUserMutation(
    $email: String!,
    $organization: String!,
    $phoneNumber: String!,
    $projectName: String,
    $responsibility: String,
    $role: String!
    ) {
    grantUserAccess (
      email: $email,
      organization: $organization,
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
        organization
        firstLogin
        lastLogin
      }
    }
  }
  `;

export const EDIT_USER_MUTATION: DocumentNode = gql`
  mutation EditUserMutation(
    $email: String!,
    $organization: String!,
    $phoneNumber: String!,
    $projectName: String!,
    $responsibility: String!,
    $role: String!
    ) {
    editUser (
      email: $email,
      organization: $organization,
      phoneNumber: $phoneNumber,
      projectName: $projectName,
      responsibility: $responsibility,
      role: $role) {
      success
    }
  }
  `;
