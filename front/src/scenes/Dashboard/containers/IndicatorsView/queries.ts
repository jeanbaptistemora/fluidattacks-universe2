import { gql } from "apollo-boost";
import { DocumentNode } from "graphql";

export const GET_INDICATORS: DocumentNode = gql`
  query GetIndicatorsQuery($projectName: String!) {
    project(projectName: $projectName){
      closedVulnerabilities
      currentMonthAuthors
      currentMonthCommits
      lastClosingVuln
      maxOpenSeverity
      maxSeverity
      meanRemediate
      openVulnerabilities
      pendingClosingCheck
      totalFindings
      totalTreatment
    }
    resources(projectName: $projectName){
      repositories
    }
  }
  `;
