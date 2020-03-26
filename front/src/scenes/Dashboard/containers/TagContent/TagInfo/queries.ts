import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const TAG_QUERY: DocumentNode = gql`
  query GetTagInfo($tag: String!) {
    tag(tag: $tag) {
      name
      projects {
        closedVulnerabilities
        name
        openVulnerabilities
      }
    }
  }
`;
