import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const UPDATE_EVENT_AFFECTATIONS: DocumentNode = gql`
  mutation updateEventAffectations(
    $eventId: String!
    $findingId: String!
    $justification: String!
    $vulnerabilities: [String]!
  ) {
    updateEventAffectations(
      eventId: $eventId
      findingId: $findingId
      justification: $justification
      vulnerabilities: $vulnerabilities
    ) {
      success
    }
  }
`;

export { UPDATE_EVENT_AFFECTATIONS };
