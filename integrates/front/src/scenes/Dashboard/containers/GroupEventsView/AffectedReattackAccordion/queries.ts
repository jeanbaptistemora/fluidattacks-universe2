import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_UNSOLVED_EVENTS: DocumentNode = gql`
  query GetUnsolvedEventsQuery($groupName: String!) {
    group(groupName: $groupName) {
      events {
        detail
        id
        eventStatus
        eventType
      }
      name
    }
  }
`;

const REQUEST_VULNS_HOLD: DocumentNode = gql`
  mutation RequestVulnerabilitiesHold(
    $eventId: String!
    $findingId: String!
    $groupName: String!
    $vulnerabilities: [String]!
  ) {
    requestVulnerabilitiesHold(
      eventId: $eventId
      findingId: $findingId
      groupName: $groupName
      vulnerabilities: $vulnerabilities
    ) {
      success
    }
  }
`;

const GET_REATTACK_VULNS: DocumentNode = gql`
  query GetReattackVulns($groupName: String!) {
    group(groupName: $groupName) {
      findings {
        id
        title
        vulnerabilitiesToReattack {
          findingId
          id
          where
          specific
        }
      }
      name
    }
  }
`;

export { GET_UNSOLVED_EVENTS, GET_REATTACK_VULNS, REQUEST_VULNS_HOLD };
