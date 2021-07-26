import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FINDING_MACHINE_JOBS: DocumentNode = gql`
  query GetFindingMachineJobs($findingId: String!, $groupName: String!) {
    finding(identifier: $findingId) {
      machineJobs {
        createdAt
        exitCode
        exitReason
        id
        name
        queue
        rootNickname
        startedAt
        stoppedAt
        status
      }
    }
    group(groupName: $groupName) {
      name
      roots {
        ... on GitRoot {
          nickname
        }
      }
    }
  }
`;

export { GET_FINDING_MACHINE_JOBS };
