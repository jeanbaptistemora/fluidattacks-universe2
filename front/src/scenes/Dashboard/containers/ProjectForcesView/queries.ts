import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_FORCES_EXECUTIONS: DocumentNode = gql`
  query GetForcesExecutions($projectName: String!) {
    forcesExecutions(projectName: $projectName) {
      executions {
        date
        exitCode
        gitRepo
        execution_id
        kind
        log
        strictness
        vulnerabilities {
          acceptedExploits {
            kind
            who
            where
            state
            exploitability
          }
          exploits {
            kind
            who
            where
            state
            exploitability
          }
          integratesExploits {
            kind
            who
            where
            state
            exploitability
          }
          numOfVulnerabilitiesInAcceptedExploits
          numOfVulnerabilitiesInExploits
          numOfVulnerabilitiesInIntegratesExploits
        }
      }
    }
  }
`;
