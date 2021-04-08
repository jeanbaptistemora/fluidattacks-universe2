import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const PORTFOLIO_GROUP_QUERY: DocumentNode = gql`
  query GetPortfoliosGroups($tag: String!) {
    tag(tag: $tag) {
      name
      projects {
        description
        name
      }
    }
  }
`;
