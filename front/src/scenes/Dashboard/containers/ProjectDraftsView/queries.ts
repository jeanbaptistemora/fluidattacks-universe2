import { gql } from "apollo-boost";
import { DocumentNode } from "graphql";

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
      }
    }
  }
`;

export const CREATE_DRAFT_MUTATION: DocumentNode = gql`
  mutation CreateDraftMutation($projectName: String!, $title: String!) {
    createDraft(projectName: $projectName, title: $title) {
      success
    }
  }
`;
