import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

import { VULNS_FRAGMENT } from "./containers/VulnerabilitiesView/queries";

const ACCEPT_LEGAL_MUTATION: DocumentNode = gql`
  mutation AcceptLegalMutation($remember: Boolean!) {
    acceptLegal(remember: $remember) {
      success
    }
  }
`;

const ACKNOWLEDGE_CONCURRENT_SESSION: DocumentNode = gql`
  mutation AcknowledgeConcurrentSessionMutation {
    acknowledgeConcurrentSession {
      success
    }
  }
`;

const ADD_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation AddStakeholderMutation($email: String!, $role: StakeholderRole!) {
    addStakeholder(email: $email, role: $role) {
      success
      email
    }
  }
`;

const GET_ORG_LEVEL_PERMISSIONS: DocumentNode = gql`
  query GetOrgLevelPermissions($identifier: String!) {
    organization(organizationId: $identifier) {
      name
      permissions(identifier: $identifier)
      userRole(identifier: $identifier)
    }
  }
`;

const GET_GROUP_LEVEL_PERMISSIONS: DocumentNode = gql`
  query GetGroupLevelPermissions($identifier: String!) {
    group(groupName: $identifier) {
      name
      permissions
      userRole
    }
  }
`;

const GET_ROOT_IDS: DocumentNode = gql`
  query GetRootIds($groupName: String!) {
    group(groupName: $groupName) {
      name
      roots {
        ... on GitRoot {
          __typename
          id
          nickname
          state
        }
        ... on IPRoot {
          __typename
          id
          nickname
          state
        }
        ... on URLRoot {
          __typename
          id
          nickname
          state
        }
      }
    }
  }
`;
const GET_USER: DocumentNode = gql`
  query GetUser {
    me(callerOrigin: "FRONT") {
      isConcurrentSession
      permissions
      phone {
        callingCountryCode
        nationalNumber
      }
      remember
      role
      sessionExpiration
      userEmail
      userName
    }
  }
`;

const GET_USER_ORGANIZATIONS_GROUPS: DocumentNode = gql`
  query GetUserOrganizationsGroups {
    me(callerOrigin: "FRONT") {
      organizations {
        groups {
          name
          permissions
          serviceAttributes
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

const GET_ME_VULNERABILITIES_ASSIGNED: DocumentNode = gql`
  query GetMeVulnerabilitiesAssigned {
    me(callerOrigin: "FRONT") {
      vulnerabilitiesAssigned {
        groupName
        ...vulnFields
      }
      userEmail
    }
  }
  ${VULNS_FRAGMENT}
`;

export {
  ACCEPT_LEGAL_MUTATION,
  ACKNOWLEDGE_CONCURRENT_SESSION,
  ADD_STAKEHOLDER_MUTATION,
  GET_ME_VULNERABILITIES_ASSIGNED,
  GET_USER,
  GET_ORG_LEVEL_PERMISSIONS,
  GET_GROUP_LEVEL_PERMISSIONS,
  GET_ROOT_IDS,
  GET_USER_ORGANIZATIONS_GROUPS,
  GET_VULNS_GROUPS,
};
