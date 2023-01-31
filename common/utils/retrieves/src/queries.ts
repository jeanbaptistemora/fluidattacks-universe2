import type { DocumentNode } from "@apollo/client/core";
import { gql } from "@apollo/client/core";

const GET_GROUPS: DocumentNode = gql`
  query GetGroups {
    me {
      userEmail
      organizations {
        groups {
          name
          subscription
        }
      }
    }
  }
`;

const GET_GIT_ROOTS = gql`
  query GetGitRoots($groupName: String!) {
    group(groupName: $groupName) {
      roots {
        ... on GitRoot {
          id
          nickname
          downloadUrl
          gitignore
          state
        }
      }
    }
  }
`;
const GET_TOE_LINES = gql`
  query GetToeLines(
    $groupName: String!
    $after: String
    $bePresent: Boolean
    $first: Int
    $rootId: ID
  ) {
    group(groupName: $groupName) {
      name
      toeLines(
        bePresent: $bePresent
        after: $after
        first: $first
        rootId: $rootId
      ) {
        edges {
          node {
            attackedLines
            filename
            comments
            modifiedDate
            loc
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
        total
        __typename
      }
      __typename
    }
  }
`;

const UPDATE_TOE_LINES_ATTACKED = gql`
  mutation UpdateToeLinesAttackedLines(
    $groupName: String!
    $fileName: String!
    $rootId: String!
    $comments: String!
  ) {
    updateToeLinesAttackedLines(
      groupName: $groupName
      filename: $fileName
      rootId: $rootId
      comments: $comments
    ) {
      success
    }
  }
`;

const GET_VULNERABILITIES = gql`
  query GetRootVulnerabilities($groupName: String!, $rootId: ID!) {
    root(groupName: $groupName, rootId: $rootId) {
      ... on GitRoot {
        nickname
        vulnerabilities {
          id
          where
          specific
        }
      }
    }
  }
`;

export {
  GET_GROUPS,
  GET_GIT_ROOTS,
  GET_TOE_LINES,
  GET_VULNERABILITIES,
  UPDATE_TOE_LINES_ATTACKED,
};
