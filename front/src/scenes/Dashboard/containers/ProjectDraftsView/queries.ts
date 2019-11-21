import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_DRAFTS: DocumentNode = gql`
  query GetDraftsQuery($projectName: String!) {
    project(projectName: $projectName){
      drafts {
        id
        reportDate
        type
        title
        description
        severityScore
        openVulnerabilities
        isExploitable
        releaseDate
        currentState
      }
    }
  }
`;

export const CREATE_DRAFT_MUTATION: DocumentNode = gql`
  mutation CreateDraftMutation(
    $cwe: String,
    $description: String,
    $projectName: String!,
    $recommendation: String,
    $requirements: String,
    $risk: String,
    $threat: String,
    $title: String!,
    $type: FindingType
    ) {
    createDraft(
      cwe: $cwe,
      description: $description,
      projectName: $projectName,
      recommendation: $recommendation,
      requirements: $requirements,
      risk: $risk,
      threat: $threat,
      title: $title,
      type: $type
    ) {
      success
    }
  }
`;
