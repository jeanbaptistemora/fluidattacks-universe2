import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_ROOTS: DocumentNode = gql`
  query GetRoots($groupName: String!) {
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
  mutation SubmitMachineJob($findingId: String!, $rootNicknames: [String!]!) {
    submitMachineJob(findingId: $findingId, rootNicknames: $rootNicknames) {
      message
      success
    }
  }
`;

export { SUBMIT_MACHINE_JOB, GET_ROOTS };
