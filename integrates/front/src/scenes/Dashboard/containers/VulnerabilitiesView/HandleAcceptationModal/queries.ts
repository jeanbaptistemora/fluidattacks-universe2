import type { DocumentNode } from "graphql";
import gql from "graphql-tag";

const HANDLE_VULNS_ACCEPTATION: DocumentNode = gql`
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

export { CONFIRM_ZERO_RISK_VULN, HANDLE_VULNS_ACCEPTATION };
