import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FORCES_EXECUTIONS: DocumentNode = gql`
  query GetForcesExecutions($projectName: String!) {
    forcesExecutions(projectName: $projectName) {
      executions {
        projectName
        date
        exitCode
        gitRepo
        execution_id
        kind
        strictness
        vulnerabilities {
          numOfAcceptedVulnerabilities
          numOfOpenVulnerabilities
          numOfClosedVulnerabilities
        }
      }
    }
  }
`;
const GET_FORCES_EXECUTION: DocumentNode = gql`
  query GetForcesExecution($projectName: String!, $executionId: String!) {
    forcesExecution(projectName: $projectName, executionId: $executionId) {
      projectName
      log
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
`;

export { GET_FORCES_EXECUTION, GET_FORCES_EXECUTIONS };
