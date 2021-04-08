import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_SEVERITY: DocumentNode = gql`
  query GetSeverityQuery($identifier: String!) {
    finding(identifier: $identifier) {
      id
      cvssVersion
      severityScore
      severity
    }
  }
`;

const UPDATE_SEVERITY_MUTATION: DocumentNode = gql`
  mutation UpdateSeverityMutation($findingId: String!, $data: GenericScalar!) {
    updateSeverity(findingId: $findingId, data: $data) {
      success
      finding {
        cvssVersion
        severity
      }
    }
  }
`;

export { GET_SEVERITY, UPDATE_SEVERITY_MUTATION };
