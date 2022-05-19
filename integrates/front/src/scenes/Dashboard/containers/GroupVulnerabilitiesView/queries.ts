import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_GROUP_FINDINGS: DocumentNode = gql`
  query GetGroupFindings($groupName: String!) {
    group(groupName: $groupName) {
      findings {
        id
        title
      }
      name
    }
  }
`;

const GET_FINDING_VULNERABILITIES: DocumentNode = gql`
  query GetFindingVulnerabilities(
    $after: String
    $findingId: String!
    $first: Int
  ) {
    finding(identifier: $findingId) {
      id
      vulnerabilitiesConnection(after: $after, first: $first) {
        edges {
          node {
            id
            where
            specific
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
      }
    }
  }
`;

export { GET_FINDING_VULNERABILITIES, GET_GROUP_FINDINGS };
