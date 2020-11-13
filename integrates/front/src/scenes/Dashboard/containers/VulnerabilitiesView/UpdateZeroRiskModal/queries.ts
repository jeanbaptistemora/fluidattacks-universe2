import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const REQUEST_ZERO_RISK_VULN: DocumentNode = gql`
mutation RequestVerificationVuln ($findingId: String!, $justification: String!, $vulnerabilities: [String]!){
  requestZeroRiskVuln(findingId: $findingId, justification: $justification, vulnerabilities: $vulnerabilities) {
    success
  }
}`;
