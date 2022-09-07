/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_DRAFTS_AND_FINDING_TITLES: DocumentNode = gql`
  query GetDraftsQuery($groupName: String!) {
    group(groupName: $groupName) {
      drafts {
        id
        reportDate
        title
        description
        severityScore
        openVulnerabilities
        isExploitable
        releaseDate
        currentState
      }
      findings {
        id
        title
      }
      language
      name
    }
  }
`;

const ADD_DRAFT_MUTATION: DocumentNode = gql`
  mutation AddDraftMutation(
    $attackComplexity: String
    $attackVector: String
    $attackVectorDescription: String
    $availabilityImpact: String
    $confidentialityImpact: String
    $description: String
    $exploitability: String
    $groupName: String!
    $integrityImpact: String
    $privilegesRequired: String
    $recommendation: String
    $minTimeToRemediate: String
    $remediationLevel: String
    $reportConfidence: String
    $requirements: String
    $severityScope: String
    $threat: String
    $title: String!
    $userInteraction: String
  ) {
    addDraft(
      attackComplexity: $attackComplexity
      attackVector: $attackVector
      attackVectorDescription: $attackVectorDescription
      availabilityImpact: $availabilityImpact
      confidentialityImpact: $confidentialityImpact
      description: $description
      exploitability: $exploitability
      groupName: $groupName
      integrityImpact: $integrityImpact
      privilegesRequired: $privilegesRequired
      recommendation: $recommendation
      minTimeToRemediate: $minTimeToRemediate
      remediationLevel: $remediationLevel
      reportConfidence: $reportConfidence
      requirements: $requirements
      severityScope: $severityScope
      threat: $threat
      title: $title
      userInteraction: $userInteraction
    ) {
      success
    }
  }
`;

const GET_ME_HAS_DRAFTS_REJECTED: DocumentNode = gql`
  query GetMeHasDraftsRejected {
    me {
      hasDraftsRejected
      userEmail
    }
  }
`;
export {
  ADD_DRAFT_MUTATION,
  GET_DRAFTS_AND_FINDING_TITLES,
  GET_ME_HAS_DRAFTS_REJECTED,
};
