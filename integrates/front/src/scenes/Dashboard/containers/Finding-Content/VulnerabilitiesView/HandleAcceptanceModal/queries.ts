import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const HANDLE_VULNS_ACCEPTANCE: DocumentNode = gql`
  mutation HandleVulnerabilitiesAcceptance(
    $acceptedVulnerabilities: [String]!
    $findingId: String!
    $justification: String!
    $rejectedVulnerabilities: [String]!
  ) {
    handleVulnerabilitiesAcceptance(
      findingId: $findingId
      justification: $justification
      acceptedVulnerabilities: $acceptedVulnerabilities
      rejectedVulnerabilities: $rejectedVulnerabilities
    ) {
      success
    }
  }
`;

const CONFIRM_VULNERABILITIES_ZERO_RISK: DocumentNode = gql`
  mutation ConfirmVulnerabilitiesZeroRisk(
    $findingId: String!
    $justification: String!
    $vulnerabilities: [String]!
  ) {
    confirmVulnerabilitiesZeroRisk(
      findingId: $findingId
      justification: $justification
      vulnerabilities: $vulnerabilities
    ) {
      success
    }
  }
`;

const REJECT_VULNERABILITIES_ZERO_RISK: DocumentNode = gql`
  mutation RejectVulnerabilitiesZeroRisk(
    $findingId: String!
    $justification: String!
    $vulnerabilities: [String]!
  ) {
    rejectVulnerabilitiesZeroRisk(
      findingId: $findingId
      justification: $justification
      vulnerabilities: $vulnerabilities
    ) {
      success
    }
  }
`;

export {
  CONFIRM_VULNERABILITIES_ZERO_RISK,
  HANDLE_VULNS_ACCEPTANCE,
  REJECT_VULNERABILITIES_ZERO_RISK,
};
