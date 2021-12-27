import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_ORGANIZATION_BILLING: DocumentNode = gql`
  query GetOrganizationBilling($organizationId: String!) {
    organization(organizationId: $organizationId) {
      name
      groups {
        name
        hasForces
        hasMachine
        hasSquad
        service
        tier
      }
    }
  }
`;
