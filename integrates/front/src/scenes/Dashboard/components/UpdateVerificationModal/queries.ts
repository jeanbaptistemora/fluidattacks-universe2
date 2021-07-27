import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const REQUEST_VULNERABILITIES_VERIFICATION: DocumentNode = gql`
  mutation requestVulnerabilitiesVerification(
    $findingId: String!
    $justification: String!
    $vulnerabilities: [String]!
  ) {
    requestVulnerabilitiesVerification(
      findingId: $findingId
      justification: $justification
      vulnerabilities: $vulnerabilities
    ) {
      success
    }
  }
`;

const VERIFY_VULNERABILITIES: DocumentNode = gql`
  mutation VerifyVulnerabilitiesRequest(
    $findingId: String!
    $justification: String!
    $openVulns: [String]!
    $closedVulns: [String]!
  ) {
    verifyVulnerabilitiesRequest(
      findingId: $findingId
      justification: $justification
      openVulnerabilities: $openVulns
      closedVulnerabilities: $closedVulns
    ) {
      success
    }
  }
`;

export { REQUEST_VULNERABILITIES_VERIFICATION, VERIFY_VULNERABILITIES };
