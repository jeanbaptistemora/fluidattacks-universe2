import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_ORGANIZATION_GROUPS: DocumentNode = gql`
  query GetOrganizationGroups($organizationId: String!) {
    organization(organizationId: $organizationId) {
      coveredAuthors
      coveredRepositories
      missedAuthors
      missedRepositories
      name
      groups {
        name
        description
        hasMachine
        hasSquad
        openFindings
        service
        subscription
        userRole
        events {
          eventStatus
        }
        managed
      }
      trial {
        completed
        extensionDate
        extensionDays
        startDate
        state
      }
    }
  }
`;
