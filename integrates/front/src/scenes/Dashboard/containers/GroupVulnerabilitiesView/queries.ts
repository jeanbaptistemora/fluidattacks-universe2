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
    rootNickname
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

const GET_GROUP_VULNERABILITIES: DocumentNode = gql`
  query GetFindingVulnerabilities(
    $after: String
    $first: Int
    $groupName: String!
    $search: String
    $treatment: String
    $stateStatus: String
    $verificationStatus: String
  ) {
    group(groupName: $groupName) {
      name
      vulnerabilities(
        after: $after
        first: $first
        search: $search
        treatment: $treatment
        stateStatus: $stateStatus
        verificationStatus: $verificationStatus
      ) {
        edges {
          node {
            groupName
            finding {
              id
              severityScore
              title
            }
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

export { GET_GROUP_VULNERABILITIES };
