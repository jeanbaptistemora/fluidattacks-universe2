import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_MACHINE_EXECUTIONS: DocumentNode = gql`
  query GetMachineExecutions($groupName: String!) {
    group(groupName: $groupName) {
      name
      roots {
        ... on GitRoot {
          id
          nickname
          machineExecutions {
            jobId
            createdAt
            startedAt
            stoppedAt
            name
            queue
            findingsExecuted {
              open
              finding
              modified
            }
          }
        }
      }
    }
  }
`;

export { GET_MACHINE_EXECUTIONS };
