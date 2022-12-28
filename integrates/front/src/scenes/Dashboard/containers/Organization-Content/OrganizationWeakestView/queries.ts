import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_ORGANIZATION_INTEGRATION_REPOSITORIES: DocumentNode = gql`
  query GetOrganizationIntegrationRepositories(
    $organizationId: String!
    $first: Int
    $after: String
  ) {
    organization(organizationId: $organizationId) {
      __typename
      name
      integrationRepositoriesConnection(after: $after, first: $first) {
        __typename
        edges {
          node {
            defaultBranch
            lastCommitDate
            url
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  }
`;

const GET_ORGANIZATION_GROUPS: DocumentNode = gql`
  query GeOrganizationGroups($organizationId: String!) {
    organization(organizationId: $organizationId) {
      __typename
      groups {
        name
        permissions
        serviceAttributes
      }
      name
      permissions
    }
  }
`;

export { GET_ORGANIZATION_INTEGRATION_REPOSITORIES, GET_ORGANIZATION_GROUPS };
