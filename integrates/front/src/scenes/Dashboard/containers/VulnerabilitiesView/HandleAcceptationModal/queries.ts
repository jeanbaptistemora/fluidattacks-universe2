import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const HANDLE_VULNS_ACCEPTATION: DocumentNode = gql`
  mutation HandleVulnsAcceptation(
    $acceptedVulns: [String]!
    $findingId: String!
    $justification: String!
    $rejectedVulns: [String]!
  ) {
    handleVulnerabilitiesAcceptation(
      findingId: $findingId
      justification: $justification
      acceptedVulnerabilities: $acceptedVulns
      rejectedVulnerabilities: $rejectedVulns
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

const REJECT_ZERO_RISK_VULNERABILITIES: DocumentNode = gql`
  mutation RejectZeroRiskVulnerabilities(
    $findingId: String!
    $justification: String!
    $vulnerabilities: [String]!
  ) {
    rejectZeroRiskVulnerabilities(
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
  HANDLE_VULNS_ACCEPTATION,
  REJECT_ZERO_RISK_VULNERABILITIES,
};
