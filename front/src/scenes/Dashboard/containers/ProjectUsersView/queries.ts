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

export const ADD_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation GrantStakeholderMutation(
    $email: String!,
    $phoneNumber: String,
    $projectName: String,
    $responsibility: String,
    $role: UserRole!
    ) {
    grantStakeholderAccess (
      email: $email,
      phoneNumber: $phoneNumber,
      projectName: $projectName,
      responsibility: $responsibility,
      role: $role) {
      success
      grantedStakeholder {
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
