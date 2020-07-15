import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_USER: DocumentNode = gql`
  query GetUserDataQuery(
    $entity: Entity!,
    $organizationId: String,
    $projectName: String,
    $userEmail: String!
  ) {
    user(
      entity: $entity,
      organizationId: $organizationId,
      projectName: $projectName,
      userEmail: $userEmail
    ) {
      email
      responsibility
      phoneNumber
    }
  }
  `;
