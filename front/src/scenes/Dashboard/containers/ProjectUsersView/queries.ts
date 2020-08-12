import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_STAKEHOLDERS: DocumentNode = gql`
  query GetStakeholdersQuery($projectName: String!) {
    project(projectName: $projectName){
      stakeholders {
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

export const REMOVE_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation RemoveStakeholderAccessMutation($projectName: String!, $userEmail: String!, ) {
    removeStakeholderAccess (
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

export const EDIT_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation EditStakeholderMutation(
    $email: String!,
    $phoneNumber: String!,
    $projectName: String!,
    $responsibility: String!,
    $role: UserRole!
    ) {
    editStakeholder (
      email: $email,
      phoneNumber: $phoneNumber,
      projectName: $projectName,
      responsibility: $responsibility,
      role: $role) {
      success
    }
  }
  `;
