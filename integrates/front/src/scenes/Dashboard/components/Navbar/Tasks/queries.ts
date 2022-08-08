import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_ME_VULNERABILITIES_ASSIGNED_IDS: DocumentNode = gql`
  query GetMeVulnerabilitiesAssignedIds {
    me(callerOrigin: "FRONT") {
      vulnerabilitiesAssigned {
        id
      }
      userEmail
    }
  }
`;

export { GET_ME_VULNERABILITIES_ASSIGNED_IDS };
