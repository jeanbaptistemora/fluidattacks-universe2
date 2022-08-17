import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_GROUP_FINDINGS: DocumentNode = gql`
  query GetGroupFindings($groupName: String!) {
    group(groupName: $groupName) {
      findings {
        id
        severityScore
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
    $where: String
  ) {
    finding(identifier: $findingId) {
      id
      vulnerabilitiesConnection(after: $after, first: $first, where: $where) {
        edges {
          node {
            currentState
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

const GET_GROUP_VULNERABILITIES: DocumentNode = gql`
  query GetFindingVulnerabilities($groupName: String!) {
    group(groupName: $groupName) {
      name
      vulnerabilities {
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
      }
    }
  }
`;

export {
  GET_FINDING_VULNERABILITIES,
  GET_GROUP_FINDINGS,
  GET_GROUP_VULNERABILITIES,
};
