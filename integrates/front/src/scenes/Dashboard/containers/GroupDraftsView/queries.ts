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

const CREATE_DRAFT_MUTATION: DocumentNode = gql`
  mutation CreateDraftMutation(
    $cwe: String
    $description: String
    $groupName: String!
    $recommendation: String
    $requirements: String
    $risk: String
    $threat: String
    $title: String!
    $type: FindingType
  ) {
    createDraft(
      cwe: $cwe
      description: $description
      projectName: $groupName
      recommendation: $recommendation
      requirements: $requirements
      risk: $risk
      threat: $threat
      title: $title
      type: $type
    ) {
      success
    }
  }
`;

export { CREATE_DRAFT_MUTATION, GET_DRAFTS };
