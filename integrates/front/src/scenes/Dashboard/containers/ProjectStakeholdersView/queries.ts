import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_STAKEHOLDERS: DocumentNode = gql`
  query GetStakeholdersQuery($projectName: String!) {
    project(projectName: $projectName) {
      name
      stakeholders {
        email
        invitationState
        role
        responsibility
        phoneNumber
        firstLogin
        lastLogin
      }
    }
  }
`;

const REMOVE_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation RemoveStakeholderAccessMutation(
    $projectName: String!
    $userEmail: String!
  ) {
    removeStakeholderAccess(projectName: $projectName, userEmail: $userEmail) {
      removedEmail
      success
    }
  }
`;

const ADD_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation GrantStakeholderMutation(
    $email: String!
    $phoneNumber: String
    $projectName: String
    $responsibility: String
    $role: StakeholderRole!
  ) {
    grantStakeholderAccess(
      email: $email
      phoneNumber: $phoneNumber
      projectName: $projectName
      responsibility: $responsibility
      role: $role
    ) {
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

const EDIT_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation EditStakeholderMutation(
    $email: String!
    $phoneNumber: String!
    $projectName: String!
    $responsibility: String!
    $role: StakeholderRole!
  ) {
    editStakeholder(
      email: $email
      phoneNumber: $phoneNumber
      projectName: $projectName
      responsibility: $responsibility
      role: $role
    ) {
      success
    }
  }
`;

export {
  GET_STAKEHOLDERS,
  REMOVE_STAKEHOLDER_MUTATION,
  ADD_STAKEHOLDER_MUTATION,
  EDIT_STAKEHOLDER_MUTATION,
};
