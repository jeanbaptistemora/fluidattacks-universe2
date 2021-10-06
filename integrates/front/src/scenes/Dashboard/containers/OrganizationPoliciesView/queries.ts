import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_ORGANIZATION_POLICIES: DocumentNode = gql`
  query GetOrganizationPolicies($organizationId: String!) {
    organization(organizationId: $organizationId) {
      findingPolicies {
        id
        lastStatusUpdate
        name
        status
        tags
      }
      maxAcceptanceDays
      maxAcceptanceSeverity
      maxNumberAcceptances
      minAcceptanceSeverity
      name
    }
  }
`;

const UPDATE_ORGANIZATION_POLICIES: DocumentNode = gql`
  mutation UpdateOrganizationPolicies(
    $maxAcceptanceDays: Int
    $maxAcceptanceSeverity: Float
    $maxNumberAcceptances: Int
    $minAcceptanceSeverity: Float
    $organizationId: String!
    $organizationName: String!
  ) {
    updateOrganizationPolicies(
      maxAcceptanceDays: $maxAcceptanceDays
      maxAcceptanceSeverity: $maxAcceptanceSeverity
      maxNumberAcceptances: $maxNumberAcceptances
      minAcceptanceSeverity: $minAcceptanceSeverity
      organizationId: $organizationId
      organizationName: $organizationName
    ) {
      success
    }
  }
`;

export { GET_ORGANIZATION_POLICIES, UPDATE_ORGANIZATION_POLICIES };
