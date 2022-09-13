/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const VULNS_FRAGMENT: DocumentNode = gql`
  fragment vulnFields on Vulnerability {
    currentState
    externalBugTrackingSystem
    findingId
    id
    lastTreatmentDate
    lastVerificationDate
    remediated
    reportDate
    severity
    specific
    stream
    tag
    treatment
    treatmentAcceptanceDate
    treatmentAcceptanceStatus
    treatmentAssigned
    treatmentJustification
    treatmentUser
    verification
    vulnerabilityType
    where
    zeroRisk
  }
`;

const GET_FINDING_AND_GROUP_INFO: DocumentNode = gql`
  query GetFindingInfo($findingId: String!) {
    finding(identifier: $findingId) {
      id
      remediated
      releaseDate
      state
      verified
    }
  }
`;

const GET_FINDING_NZR_VULNS: DocumentNode = gql`
  query GetFindingNzrVulns(
    $after: String
    $findingId: String!
    $first: Int
    $state: VulnerabilityState
  ) {
    finding(identifier: $findingId) {
      __typename
      id
      vulnerabilitiesConnection(after: $after, first: $first, state: $state) {
        edges {
          node {
            ...vulnFields
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
      }
    }
  }
  ${VULNS_FRAGMENT}
`;

const GET_FINDING_ZR_VULNS: DocumentNode = gql`
  query GetFindingZrVulns(
    $after: String
    $canRetrieveZeroRisk: Boolean!
    $findingId: String!
    $first: Int
  ) {
    finding(identifier: $findingId) {
      __typename
      id
      zeroRiskConnection(after: $after, first: $first)
        @include(if: $canRetrieveZeroRisk) {
        edges {
          node {
            ...vulnFields
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
      }
    }
  }
  ${VULNS_FRAGMENT}
`;

const SEND_VULNERABILITY_NOTIFICATION: DocumentNode = gql`
  mutation SendVulnerabilityNotification($findingId: String!) {
    sendVulnerabilityNotification(findingId: $findingId) {
      success
    }
  }
`;

export {
  VULNS_FRAGMENT,
  GET_FINDING_AND_GROUP_INFO,
  GET_FINDING_NZR_VULNS,
  GET_FINDING_ZR_VULNS,
  SEND_VULNERABILITY_NOTIFICATION,
};
