import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const ADD_ORGANIZATION_FINDING_POLICY: DocumentNode = gql`
  mutation AddOrgFindingPolicy($name: String!, $organizationName: String!) {
    addOrgFindingPolicy(
      findingName: $name
      organizationName: $organizationName
    ) {
      success
    }
  }
`;

const GET_ORGANIZATION_FINDINGS_TITLES: DocumentNode = gql`
  query GetOrganizationFindingTitles($organizationId: String!) {
    organization(organizationId: $organizationId) {
      id
      name
      projects {
        name
        findings {
          id
          title
        }
      }
    }
  }
`;

export { ADD_ORGANIZATION_FINDING_POLICY, GET_ORGANIZATION_FINDINGS_TITLES };
