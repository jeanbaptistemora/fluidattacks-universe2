import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_ORGANIZATION_ID: DocumentNode = gql`
  query GetOrganizationId($organizationName: String!) {
    organizationId(organizationName: $organizationName) {
      id
      name
    }
  }
`;

const GET_USER_PORTFOLIOS: DocumentNode = gql`
  query GetUserPortfolios($organizationId: String!) {
    me(callerOrigin: "FRONT") {
      tags(organizationId: $organizationId) {
        name
        groups {
          name
        }
      }
      userEmail
    }
  }
`;

export { GET_ORGANIZATION_ID, GET_USER_PORTFOLIOS };
