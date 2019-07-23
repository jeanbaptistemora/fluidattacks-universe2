import { gql } from "apollo-boost";
import { DocumentNode } from "graphql";

export const GET_VULNERABILITIES: DocumentNode = gql`
  query GetVulnerabilitiesQuery($identifier: String!) {
    finding(identifier: $identifier) {
      id
      releaseDate
      portsVulns: vulnerabilities(
        vulnType: "ports") {
        ...vulnInfo
      }
      linesVulns: vulnerabilities(
        vulnType: "lines") {
        ...vulnInfo
      }
      inputsVulns: vulnerabilities(
        vulnType: "inputs") {
        ...vulnInfo
      }
    }
  }
  fragment vulnInfo on Vulnerability {
    vulnType
    where
    specific
    currentState
    id
    findingId
    treatment
  }
  `;

export const UPDATE_TREATMENT_MUTATION: DocumentNode = gql`
  mutation UpdateTreatmentMutation( $data: GenericScalar!, $findingId: String! ) {
    updateTreatmentVuln (
      data: $data,
      findingId: $findingId
    ){
      success
    }
  }
  `;

export const DELETE_VULN_MUTATION: DocumentNode = gql`
  mutation DeleteVulnMutation($id: String!, $findingId: String!, ) {
    deleteVulnerability (
      id: $id,
      findingId: $findingId
    ) {
      success
    }
  }
  `;
