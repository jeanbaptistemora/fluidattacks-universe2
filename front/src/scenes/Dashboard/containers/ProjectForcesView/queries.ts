import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_FORCES_EXECUTIONS: DocumentNode = gql`
  query GetBreakBuildExecutions($projectName: String!) {
    breakBuildExecutions(projectName: $projectName) {
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
            who
            where
          }
          exploits {
            kind
            who
            where
          }
          mockedExploits {
            kind
            who
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
