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
