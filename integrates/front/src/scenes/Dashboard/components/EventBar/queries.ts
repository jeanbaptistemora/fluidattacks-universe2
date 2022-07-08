import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_ORG_EVENTS: DocumentNode = gql`
  query GetOrganizationEvents($organizationName: String!) {
    organizationId(organizationName: $organizationName) {
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
