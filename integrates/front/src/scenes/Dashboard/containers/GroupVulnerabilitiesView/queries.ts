import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_GROUP_VULNERABILITIES: DocumentNode = gql`
  query GetFindingVulnerabilities(
    $after: String
    $first: Int
    $groupName: String!
    $search: String
  ) {
    group(groupName: $groupName) {
      name
      vulnerabilities(after: $after, first: $first, search: $search) {
        edges {
          node {
            currentState
            finding {
              id
              severityScore
              title
            }
            id
            reportDate
            specific
            treatment
            where
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

export { GET_GROUP_VULNERABILITIES };
