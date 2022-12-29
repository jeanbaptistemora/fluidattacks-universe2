import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_ORG_GROUPS: DocumentNode = gql`
  query GetOrgGroups($org: String!) {
    organizationId(organizationName: $org) {
      name
      groups {
        name
      }
    }
  }
`;

const GET_VULNERABLE_GROUP_VULNS: DocumentNode = gql`
  query GetGroupVulns($after: String, $first: Int, $group: String!) {
    group(groupName: $group) {
      name
      vulnerabilities(after: $after, first: $first, stateStatus: "VULNERABLE") {
        edges {
          node {
            state
            zeroRisk
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
        total
      }
    }
  }
`;

export { GET_ORG_GROUPS, GET_VULNERABLE_GROUP_VULNS };
