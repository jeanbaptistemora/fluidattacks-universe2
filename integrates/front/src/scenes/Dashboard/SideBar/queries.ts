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

const GET_GROUP_VULNS: DocumentNode = gql`
  query GetGroupVulns($group: String!) {
    group(groupName: $group) {
      name
      vulnerabilities {
        edges {
          node {
            currentState
            state
            zeroRisk
          }
        }
      }
    }
  }
`;

export { GET_ORG_GROUPS, GET_GROUP_VULNS };
