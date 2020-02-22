import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_FORCES_EXECUTIONS: DocumentNode = gql`
  query GetBreakBuildExecutions($projectName: String!) {
    breakBuildExecutions(projectName: $projectName) {
      executions {
        identifier
        date
        gitRepo
        kind
        log
        strictness
      }
    }
  }
`;
