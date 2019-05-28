import { gql } from "apollo-boost";
import { DocumentNode } from "graphql";

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
        treatment
        isExploitable
      }
    }
  }
  `;
