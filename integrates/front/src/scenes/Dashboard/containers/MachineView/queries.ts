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
          state
        }
      }
    }
  }
`;

const SUBMIT_MACHINE_JOB: DocumentNode = gql`
  mutation SubmitMachineJob($findingId: String!, $rootNickname: String!) {
    submitMachineJob(findingId: $findingId, rootNickname: $rootNickname) {
      success
    }
  }
`;

export { GET_FINDING_MACHINE_JOBS, SUBMIT_MACHINE_JOB };
