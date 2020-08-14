import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_USER: DocumentNode = gql`
  query GetStakeholderDataQuery(
    $entity: Entity!,
    $organizationId: String,
    $projectName: String,
    $userEmail: String!
  ) {
    stakeholder(
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
