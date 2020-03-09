import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_FINDINGS: DocumentNode = gql`
  query GetFindingsQuery($projectName: String!) {
    project(projectName: $projectName){
      findings {
        id
        age
        lastVulnerability
        type
        title
        description
        severityScore
        openVulnerabilities
        state
        isExploitable
        remediated
        verified
        vulnerabilities(state: "open") {
          where
        }
        historicTreatment
      }
    }
  }`;
