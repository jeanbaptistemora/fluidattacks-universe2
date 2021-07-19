import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_DRAFTS: DocumentNode = gql`
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
      language
      name
    }
  }
`;

const ADD_DRAFT_MUTATION: DocumentNode = gql`
  mutation AddDraftMutation(
    $attackComplexity: String
    $attackVector: String
    $availabilityImpact: String
    $confidentialityImpact: String
    $cwe: String
    $description: String
    $exploitability: String
    $groupName: String!
    $integrityImpact: String
    $privilegesRequired: String
    $recommendation: String
    $remediationLevel: String
    $reportConfidence: String
    $requirements: String
    $risk: String
    $severityScope: String
    $threat: String
    $title: String!
    $userInteraction: String
  ) {
    addDraft(
      attackComplexity: $attackComplexity
      attackVector: $attackVector
      availabilityImpact: $availabilityImpact
      confidentialityImpact: $confidentialityImpact
      cwe: $cwe
      description: $description
      exploitability: $exploitability
      groupName: $groupName
      integrityImpact: $integrityImpact
      privilegesRequired: $privilegesRequired
      recommendation: $recommendation
      remediationLevel: $remediationLevel
      reportConfidence: $reportConfidence
      requirements: $requirements
      risk: $risk
      severityScope: $severityScope
      threat: $threat
      title: $title
      userInteraction: $userInteraction
    ) {
      success
    }
  }
`;

export { ADD_DRAFT_MUTATION, GET_DRAFTS };
