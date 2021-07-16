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
      name
    }
  }
`;

const ADD_DRAFT_MUTATION: DocumentNode = gql`
  mutation AddDraftMutation(
    $cwe: String
    $description: String
    $groupName: String!
    $recommendation: String
    $requirements: String
    $risk: String
    $threat: String
    $title: String!
  ) {
    addDraft(
      cwe: $cwe
      description: $description
      groupName: $groupName
      recommendation: $recommendation
      requirements: $requirements
      risk: $risk
      threat: $threat
      title: $title
    ) {
      success
    }
  }
`;

export { ADD_DRAFT_MUTATION, GET_DRAFTS };
