import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const PORTFOLIO_GROUP_QUERY: DocumentNode = gql`
  query GetPortfoliosGroups($tag: String!, $organizationId: String) {
    tag(tag: $tag, organizationId: $organizationId) {
      name
      groups {
        description
        name
      }
    }
  }
`;
