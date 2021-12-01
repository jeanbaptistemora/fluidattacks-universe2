import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_TOE_LINES: DocumentNode = gql`
  query GetToeLines($groupName: String!, $after: String, $bePresent: Boolean) {
    group(groupName: $groupName) {
      name
      toeLines(bePresent: $bePresent, after: $after, first: 500) {
        edges {
          node {
            attackedAt
            attackedBy
            attackedLines
            bePresent
            bePresentUntil
            comments
            commitAuthor
            filename
            firstAttackAt
            loc
            modifiedCommit
            modifiedDate
            root {
              nickname
            }
            seenAt
            sortsRiskLevel
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
        __typename
      }
      __typename
    }
  }
`;

export { GET_TOE_LINES };
