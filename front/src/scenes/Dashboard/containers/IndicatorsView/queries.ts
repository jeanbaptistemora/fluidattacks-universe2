import { DocumentNode } from "graphql";
import gql from "graphql-tag";

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
      remediatedOverTime
      totalFindings
      totalTreatment
    }
    resources(projectName: $projectName){
      repositories
    }
  }
  `;
