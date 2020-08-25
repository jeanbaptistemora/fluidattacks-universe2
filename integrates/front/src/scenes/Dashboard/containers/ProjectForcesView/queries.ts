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
          }
          exploits {
            kind
            who
            where
          }
          integratesExploits {
            kind
            who
            where
          }
          numOfVulnerabilitiesInAcceptedExploits
          numOfVulnerabilitiesInExploits
          numOfVulnerabilitiesInIntegratesExploits
        }
      }
    }
    forcesExecutionsNew(projectName: $projectName) {
      executions {
        date
        exitCode
        gitRepo
        execution_id
        kind
        log
        strictness
        vulnerabilities {
          open {
            kind
            who
            where
            state
            exploitability
          }
          closed {
            kind
            who
            where
            state
            exploitability
          }
          accepted {
            kind
            who
            where
            state
            exploitability
          }
          numOfAcceptedVulnerabilities
          numOfOpenVulnerabilities
          numOfClosedVulnerabilities
        }
      }
    }
  }
`;
