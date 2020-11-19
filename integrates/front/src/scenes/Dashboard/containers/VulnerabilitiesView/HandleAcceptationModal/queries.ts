import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const HANDLE_VULNS_ACCEPTATION: DocumentNode = gql`
  mutation HandleVulnsAcceptation(
    $acceptedVulns: [String]!
    $findingId: String!
    $justification: String!
    $rejectedVulns: [String]!
  ) {
    handleVulnsAcceptation(
      findingId: $findingId
      justification: $justification
      acceptedVulns: $acceptedVulns
      rejectedVulns: $rejectedVulns
    ) {
      success
    }
  }`;
