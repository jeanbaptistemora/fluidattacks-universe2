import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FORCES_EXECUTIONS: DocumentNode = gql`
  query GetForcesExecutions(
    $after: String
    $first: Int
    $fromDate: DateTime
    $gitRepo: String
    $groupName: String!
    $search: String
    $status: String
    $strictness: String
    $toDate: DateTime
    $type: String
  ) {
    group(groupName: $groupName) {
      executionsConnections(
        after: $after
        first: $first
        fromDate: $fromDate
        gitRepo: $gitRepo
        search: $search
        status: $status
        strictness: $strictness
        toDate: $toDate
        type: $type
      ) {
        edges {
          node {
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
        pageInfo {
          endCursor
          hasNextPage
        }
        total
      }
      name
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
