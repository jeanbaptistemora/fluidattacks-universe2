import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_ENTITY_ORGANIZATION: DocumentNode = gql`
  query GetEntityOrganization(
    $getProject: Boolean!
    $getTag: Boolean!
    $projectName: String!
    $tagName: String!
  ) {
    project(projectName: $projectName) @include(if: $getProject) {
      organization
    }
    tag(tag: $tagName) @include(if: $getTag) {
      organization
    }
  }
`;
