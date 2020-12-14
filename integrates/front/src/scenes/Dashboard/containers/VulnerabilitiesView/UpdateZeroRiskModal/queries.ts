import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const CONFIRM_ZERO_RISK_VULN: DocumentNode = gql`
mutation ConfirmZeroRiskVuln ($findingId: String!, $justification: String!, $vulnerabilities: [String]!){
  confirmZeroRiskVuln(findingId: $findingId, justification: $justification, vulnerabilities: $vulnerabilities) {
    success
  }
}`;

export const REJECT_ZERO_RISK_VULN: DocumentNode = gql`
mutation RejectZeroRiskVuln ($findingId: String!, $justification: String!, $vulnerabilities: [String]!){
  rejectZeroRiskVuln(findingId: $findingId, justification: $justification, vulnerabilities: $vulnerabilities) {
    success
  }
}`;
