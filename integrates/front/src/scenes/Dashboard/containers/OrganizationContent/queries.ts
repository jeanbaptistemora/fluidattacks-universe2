import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_ORGANIZATION_ID: DocumentNode = gql`
  query GetOrganizationId ($organizationName: String!) {
    organizationId(organizationName: $organizationName) {
      id
  }
}
`;

export const GET_USER_PORTFOLIOS: DocumentNode = gql`
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
