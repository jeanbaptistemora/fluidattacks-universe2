import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_EVENTS: DocumentNode = gql`
  query GetEventsQuery($groupName: String!) {
    group(groupName: $groupName) {
      events {
        eventStatus
      }
      name
    }
  }
`;

export { GET_EVENTS };
