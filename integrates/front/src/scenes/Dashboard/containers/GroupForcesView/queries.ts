import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FORCES_EXECUTIONS: DocumentNode = gql`
  query GetForcesExecutions($groupName: String!) {
    forcesExecutions(groupName: $groupName) {
      executions {
        groupName
        gracePeriod
        date
        exitCode
        gitRepo
        executionId
        kind
        severityThreshold
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
  query GetForcesExecution($groupName: String!, $executionId: String!) {
    forcesExecution(groupName: $groupName, executionId: $executionId) {
      groupName
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
