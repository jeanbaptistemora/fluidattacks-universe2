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

const CONFIRM_ZERO_RISK_VULN: DocumentNode = gql`
  mutation ConfirmZeroRiskVuln(
    $findingId: String!
    $justification: String!
    $vulnerabilities: [String]!
  ) {
    confirmZeroRiskVuln(
      findingId: $findingId
      justification: $justification
      vulnerabilities: $vulnerabilities
    ) {
      success
    }
  }
`;

const REJECT_ZERO_RISK_VULN: DocumentNode = gql`
  mutation RejectZeroRiskVuln(
    $findingId: String!
    $justification: String!
    $vulnerabilities: [String]!
  ) {
    rejectZeroRiskVuln(
      findingId: $findingId
      justification: $justification
      vulnerabilities: $vulnerabilities
    ) {
      success
    }
  }
`;

export {
  CONFIRM_ZERO_RISK_VULN,
  HANDLE_VULNS_ACCEPTATION,
  REJECT_ZERO_RISK_VULN,
};
