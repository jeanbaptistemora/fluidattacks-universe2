import type { DocumentNode } from "graphql";
import gql from "graphql-tag";

const GET_ORGANIZATION_ID: DocumentNode = gql`
  query GetOrganizationId($organizationName: String!) {
    organizationId(organizationName: $organizationName) {
      id
    }
  }
`;

const GET_USER_PORTFOLIOS: DocumentNode = gql`
  query GetUserPortfolios($organizationId: String!) {
    me(callerOrigin: "FRONT") {
      tags(organizationId: $organizationId) {
        name
        projects {
          name
        }
      }
    }
  }
`;

export { GET_ORGANIZATION_ID, GET_USER_PORTFOLIOS };
