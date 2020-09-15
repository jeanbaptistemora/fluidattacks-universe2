import { DocumentNode } from "graphql";
import gql from "graphql-tag";

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
