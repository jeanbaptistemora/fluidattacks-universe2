import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

import { VULNS_FRAGMENT } from "../../Finding-Content/VulnerabilitiesView/queries";

const GET_ME_VULNERABILITIES_ASSIGNED: DocumentNode = gql`
  query GetMeVulnerabilitiesAssigned {
    me(callerOrigin: "FRONT") {
      vulnerabilitiesAssigned {
        finding {
          id
          severityScore
          title
        }
        groupName
        ...vulnFields
      }
      userEmail
    }
  }
  ${VULNS_FRAGMENT}
`;

export { GET_ME_VULNERABILITIES_ASSIGNED };
