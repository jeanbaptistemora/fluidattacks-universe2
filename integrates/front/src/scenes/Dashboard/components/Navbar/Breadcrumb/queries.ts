import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

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

export { GET_FINDING_TITLE, GET_USER_ORGANIZATIONS };
