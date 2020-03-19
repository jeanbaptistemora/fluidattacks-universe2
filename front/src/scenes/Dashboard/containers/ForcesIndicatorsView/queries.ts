import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_INDICATORS: DocumentNode = gql`
  query GetForcesIndicatorsQuery($projectName: String!) {
    forcesExecutions(projectName: $projectName) {
      executions {
        strictness
        vulnerabilities {
          numOfVulnerabilitiesInAcceptedExploits
          numOfVulnerabilitiesInExploits
          numOfVulnerabilitiesInMockedExploits
        }
      }
    }
    project(projectName: $projectName){
      hasForces
    }
  }
  `;
