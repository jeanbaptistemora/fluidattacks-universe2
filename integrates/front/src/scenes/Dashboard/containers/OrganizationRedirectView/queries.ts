import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_ENTITY_ORGANIZATION: DocumentNode = gql`
  query GetEntityOrganization(
    $getGroup: Boolean!
    $getTag: Boolean!
    $groupName: String!
    $tagName: String!
  ) {
    group(groupName: $groupName) @include(if: $getGroup) {
      name
      organization
    }
    tag(tag: $tagName) @include(if: $getTag) {
      organization
    }
  }
`;
