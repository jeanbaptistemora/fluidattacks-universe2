/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_ORGANIZATION_POLICIES: DocumentNode = gql`
  query GetOrganizationPolicies($organizationId: String!) {
    organization(organizationId: $organizationId) {
      findingPolicies {
        id
        lastStatusUpdate
        name
        status
        tags
      }
      maxAcceptanceDays
      maxAcceptanceSeverity
      maxNumberAcceptances
      minAcceptanceSeverity
      minBreakingSeverity
      vulnerabilityGracePeriod
      name
    }
  }
`;

const UPDATE_ORGANIZATION_POLICIES: DocumentNode = gql`
  mutation UpdateOrganizationPolicies(
    $maxAcceptanceDays: Int
    $maxAcceptanceSeverity: Float
    $maxNumberAcceptances: Int
    $minAcceptanceSeverity: Float
    $minBreakingSeverity: Float
    $vulnerabilityGracePeriod: Int
    $organizationId: String!
    $organizationName: String!
  ) {
    updateOrganizationPolicies(
      maxAcceptanceDays: $maxAcceptanceDays
      maxAcceptanceSeverity: $maxAcceptanceSeverity
      maxNumberAcceptances: $maxNumberAcceptances
      minAcceptanceSeverity: $minAcceptanceSeverity
      minBreakingSeverity: $minBreakingSeverity
      vulnerabilityGracePeriod: $vulnerabilityGracePeriod
      organizationId: $organizationId
      organizationName: $organizationName
    ) {
      success
    }
  }
`;

export { GET_ORGANIZATION_POLICIES, UPDATE_ORGANIZATION_POLICIES };
