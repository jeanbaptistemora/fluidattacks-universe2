import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const ADD_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation AddStakeholderMutation(
    $email: String!,
    $role: StakeholderRole!
    $phoneNumber: String,
    ) {
    addStakeholder (
      email: $email,
      role: $role,
      phoneNumber: $phoneNumber,
    ) {
      success
      email
    }
  }
`;

export const GET_USER_PERMISSIONS: DocumentNode = gql`
  query GetPermissions($entity: Entity!, $identifier: String) {
    me(callerOrigin: "FRONT") {
      permissions(entity: $entity, identifier: $identifier)
      role(entity: $entity, identifier: $identifier)
    }
  }
`;
