import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

import { VULNS_FRAGMENT } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";

const GET_FINDING_TITLE: DocumentNode = gql`
  query GetFindingTitle($findingId: String!) {
    finding(identifier: $findingId) {
      title
    }
  }
`;

const GET_USER_ORGANIZATIONS: DocumentNode = gql`
  query GetUserOrganizations {
    me(callerOrigin: "FRONT") {
      organizations {
        name
      }
      userEmail
    }
  }
`;

const GET_USER_ORGANIZATIONS_GROUPS: DocumentNode = gql`
  query GetUserOrganizationsGroups {
    me(callerOrigin: "FRONT") {
      organizations {
        groups {
          name
        }
        name
      }
      userEmail
    }
  }
`;

const GET_VULNS_GROUPS: DocumentNode = gql`
  query GetVulnerabilitiesAssigned($groupName: String!) {
    group(groupName: $groupName) {
      vulnerabilitiesAssigned {
        ...vulnFields
      }
      name
    }
  }
  ${VULNS_FRAGMENT}
`;

export {
  GET_FINDING_TITLE,
  GET_USER_ORGANIZATIONS,
  GET_USER_ORGANIZATIONS_GROUPS,
  GET_VULNS_GROUPS,
};
