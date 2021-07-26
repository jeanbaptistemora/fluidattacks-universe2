import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const REQUEST_VERIFICATION_VULNERABILITIES: DocumentNode = gql`
  mutation RequestVerificationVulnerabilities(
    $findingId: String!
    $justification: String!
    $vulnerabilities: [String]!
  ) {
    requestVerificationVulnerabilities(
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

export { REQUEST_VERIFICATION_VULNERABILITIES, VERIFY_VULNERABILITIES };
