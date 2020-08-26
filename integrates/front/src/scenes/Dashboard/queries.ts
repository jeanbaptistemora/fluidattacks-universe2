import { DocumentNode } from "graphql";
import gql from "graphql-tag";

const ADD_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation AddStakeholderMutation(
    $email: String!
    $role: StakeholderRole!
    $phoneNumber: String
  ) {
    addStakeholder(email: $email, role: $role, phoneNumber: $phoneNumber) {
      success
      email
    }
  }
`;

const GET_USER_PERMISSIONS: DocumentNode = gql`
  query GetPermissions($entity: Entity!, $identifier: String) {
    me(callerOrigin: "FRONT") {
      permissions(entity: $entity, identifier: $identifier)
      role(entity: $entity, identifier: $identifier)
    }
  }
`;

const SESSION_EXPIRATION: DocumentNode = gql`
  query sessionExpiration {
    me(callerOrigin: "FRONT") {
      sessionExpiration
    }
  }
`;

export { ADD_STAKEHOLDER_MUTATION, GET_USER_PERMISSIONS, SESSION_EXPIRATION };
