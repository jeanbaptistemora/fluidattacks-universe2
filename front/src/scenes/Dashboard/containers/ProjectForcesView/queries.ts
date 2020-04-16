import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_FORCES_EXECUTIONS: DocumentNode = gql`
  query GetForcesExecutions($projectName: String!) {
    forcesExecutions(projectName: $projectName) {
      executions {
        date
        exitCode
        gitRepo
        identifier
        kind
        log
        strictness
        vulnerabilities {
          acceptedExploits {
            kind
            what
            where
          }
          exploits {
            kind
            what
            where
          }
          mockedExploits {
            kind
            what
            where
          }
          numOfVulnerabilitiesInAcceptedExploits
          numOfVulnerabilitiesInExploits
          numOfVulnerabilitiesInMockedExploits
        }
      }
    }
  }
`;
