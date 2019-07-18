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

export const UPDATE_TREATMENT_VULN_MUTATION: DocumentNode = gql`
  mutation UpdateTreatmentVulnMutation($treatmentsInfo: GenericScalar!,
                                       $vulnerability: GenericScalar!, ) {
    updateTreatmentVulnerability(
      treatmentsInfo: $treatmentsInfo,
      vulnerability: $vulnerability
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
