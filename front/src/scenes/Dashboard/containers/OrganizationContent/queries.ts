import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_ORGANIZATION_ID: DocumentNode = gql`
  query GetOrganizationId ($organizationName: String!) {
    organizationId(organizationName: $organizationName) {
      id
  }
}
`;
