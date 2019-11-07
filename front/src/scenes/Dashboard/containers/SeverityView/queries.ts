import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_SEVERITY: DocumentNode = gql`
  query GetSeverityQuery($identifier: String!) {
    finding(identifier: $identifier){
      id
      cvssVersion
      severity
    }
  }
  `;

export const UPDATE_SEVERITY_MUTATION: DocumentNode = gql`
  mutation UpdateSeverityMutation(
      $findingId: String!,
      $data: GenericScalar!) {
    updateSeverity (
      findingId: $findingId,
      data: $data
    ) {
      success
      finding {
        cvssVersion
        severity
      }
    }
  }
  `;
