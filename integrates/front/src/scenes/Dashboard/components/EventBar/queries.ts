import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_ORG_EVENTS: DocumentNode = gql`
  query GetOrganizationId($organizationName: String!) {
    organizationId(organizationName: $organizationName) {
      id
      groups {
        events {
          eventStatus
          eventDate
          groupName
        }
        name
      }
      name
    }
  }
`;

export { GET_ORG_EVENTS };
