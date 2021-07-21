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
      acceptedVulns: $acceptedVulns
      rejectedVulns: $rejectedVulns
    ) {
      success
    }
  }
`;

const CONFIRM_ZERO_RISK_VULNERABILITIES: DocumentNode = gql`
  mutation ConfirmZeroRiskVulnerabilities(
    $findingId: String!
    $justification: String!
    $vulnerabilities: [String]!
  ) {
    confirmZeroRiskVulnerabilities(
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
  CONFIRM_ZERO_RISK_VULNERABILITIES,
  HANDLE_VULNS_ACCEPTATION,
  REJECT_ZERO_RISK_VULNERABILITIES,
};
