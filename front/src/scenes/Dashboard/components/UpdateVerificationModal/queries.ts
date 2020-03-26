import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const REQUEST_VERIFICATION_VULN: DocumentNode = gql`
mutation RequestVerificationVuln ($findingId: String!, $justification: String!, $vulnerabilities: [String]!){
  requestVerificationVuln(findingId: $findingId, justification: $justification, vulnerabilities: $vulnerabilities) {
    success
  }
}`;

export const VERIFY_VULNERABILITIES: DocumentNode = gql`
mutation VerifyRequestVuln (
  $findingId: String!, $justification: String!, $openVulns: [String]!, $closedVulns: [String]!) {
  verifyRequestVuln(
    findingId: $findingId, justification: $justification, openVulns: $openVulns,closedVulns: $closedVulns) {
    success
  }
}`;
