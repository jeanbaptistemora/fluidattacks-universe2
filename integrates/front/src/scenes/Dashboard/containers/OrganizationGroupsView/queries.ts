import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_ORGANIZATION_GROUPS: DocumentNode = gql`
  query GetOrganizationGroups($organizationId: String!) {
    organization(organizationId: $organizationId) {
      name
      groups {
        name
        description
        hasMachine
        hasSquad
        service
        subscription
        userRole
        events {
          eventStatus
        }
      }
    }
  }
`;
