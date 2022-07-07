import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_EVENTS: DocumentNode = gql`
  query GetEventsQuery($organizationName: String!) {
    organizationId(organizationName: $organizationName) {
      groups {
        name
        events {
          eventStatus
          eventDate
          groupName
        }
      }
      name
    }
  }
`;

export { GET_EVENTS };
