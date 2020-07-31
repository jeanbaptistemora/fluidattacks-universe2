import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_ORGANIZATION_GROUPS: DocumentNode = gql`
  query GetOrganizationGroups($organizationId: String!) {
    organization(organizationId: $organizationId) {
      projects {
        name
        description
        hasDrills
        hasForces
        userRole
      }
    }
  }
`;
