import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_STAKEHOLDERS: DocumentNode = gql`
  query GetStakeholdersQuery($groupName: String!) {
    group(groupName: $groupName) {
      name
      stakeholders {
        email
        invitationState
        role
        responsibility
        firstLogin
        lastLogin
      }
    }
  }
`;

const REMOVE_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation RemoveStakeholderAccessMutation(
    $groupName: String!
    $userEmail: String!
  ) {
    removeStakeholderAccess(groupName: $groupName, userEmail: $userEmail) {
      removedEmail
      success
    }
  }
`;

const ADD_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation GrantStakeholderMutation(
    $email: String!
    $groupName: String
    $responsibility: String
    $role: StakeholderRole!
  ) {
    grantStakeholderAccess(
      email: $email
      groupName: $groupName
      responsibility: $responsibility
      role: $role
    ) {
      success
      grantedStakeholder {
        email
        role
        responsibility
        firstLogin
        lastLogin
      }
    }
  }
`;

const UPDATE_GROUP_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation UpdateGroupStakeholderMutation(
    $email: String!
    $groupName: String!
    $responsibility: String!
    $role: StakeholderRole!
  ) {
    updateGroupStakeholder(
      email: $email
      groupName: $groupName
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
  UPDATE_GROUP_STAKEHOLDER_MUTATION,
};
