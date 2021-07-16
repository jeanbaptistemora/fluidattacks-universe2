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
    $attackVector: String
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
      attackVector: $attackVector
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
