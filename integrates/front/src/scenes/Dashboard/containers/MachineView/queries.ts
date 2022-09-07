/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FINDING_MACHINE_JOBS: DocumentNode = gql`
  query GetFindingMachineJobs($findingId: String!) {
    finding(identifier: $findingId) {
      id
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
        vulnerabilities {
          open
          modified
        }
      }
    }
  }
`;
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

export { GET_FINDING_MACHINE_JOBS, SUBMIT_MACHINE_JOB, GET_ROOTS };
