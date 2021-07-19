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
    $confidentialityImpact: String
    $cwe: String
    $description: String
    $groupName: String!
    $privilegesRequired: String
    $recommendation: String
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
      confidentialityImpact: $confidentialityImpact
      cwe: $cwe
      description: $description
      groupName: $groupName
      privilegesRequired: $privilegesRequired
      recommendation: $recommendation
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
