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
      deletionDate
      userDeletion
    }
    resources(projectName: $projectName){
      repositories
    }
  }
  `;

export const REJECT_REMOVE_PROJECT_MUTATION: DocumentNode = gql`
  mutation RejectProjectDeletion($projectName: String!) {
    rejectRemoveProject(projectName: $projectName) {
      success
    }
  }
`;
