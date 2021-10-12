import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_STAKEHOLDER: DocumentNode = gql`
  query GetStakeholderDataQuery(
    $entity: StakeholderEntity!
    $organizationId: String
    $groupName: String
    $userEmail: String!
  ) {
    stakeholder(
      entity: $entity
      organizationId: $organizationId
      groupName: $groupName
      userEmail: $userEmail
    ) {
      email
      responsibility
    }
  }
`;
