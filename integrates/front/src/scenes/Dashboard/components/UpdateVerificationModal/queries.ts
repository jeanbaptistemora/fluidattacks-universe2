import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const REQUEST_VERIFICATION_VULN: DocumentNode = gql`
  mutation RequestVerificationVuln(
    $findingId: String!
    $justification: String!
    $vulnerabilities: [String]!
  ) {
    requestVerificationVuln(
      findingId: $findingId
      justification: $justification
      vulnerabilities: $vulnerabilities
    ) {
      success
    }
  }
`;

const VERIFY_VULNERABILITIES: DocumentNode = gql`
  mutation VerifyRequestVulnerabilities(
    $findingId: String!
    $justification: String!
    $openVulns: [String]!
    $closedVulns: [String]!
  ) {
    verifyRequestVulnerabilities(
      findingId: $findingId
      justification: $justification
      openVulnerabilities: $openVulns
      closedVulnerabilities: $closedVulns
    ) {
      success
    }
  }
`;

export { REQUEST_VERIFICATION_VULN, VERIFY_VULNERABILITIES };
