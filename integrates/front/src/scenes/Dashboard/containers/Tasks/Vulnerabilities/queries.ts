import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

import { VULNS_FRAGMENT } from "../../VulnerabilitiesView/queries";

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

export { GET_ME_VULNERABILITIES_ASSIGNED, GET_USER_ORGANIZATIONS_GROUPS };
