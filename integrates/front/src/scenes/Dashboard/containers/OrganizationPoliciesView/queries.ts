import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_ORGANIZATION_POLICIES: DocumentNode = gql`
  query GetOrganizationPolicies($organizationId: String!) {
    organization(organizationId: $organizationId) {
      findingPolicies {
        id
        name
        status
        lastStatusUpdate
      }
      maxAcceptanceDays
      maxAcceptanceSeverity
      maxNumberAcceptations
      minAcceptanceSeverity
      name
    }
  }
`;

const UPDATE_ORGANIZATION_POLICIES: DocumentNode = gql`
  mutation UpdateOrganizationPolicies(
    $maxAcceptanceDays: Int
    $maxAcceptanceSeverity: Float
    $maxNumberAcceptations: Int
    $minAcceptanceSeverity: Float
    $organizationId: String!
    $organizationName: String!
  ) {
    updateOrganizationPolicies(
      maxAcceptanceDays: $maxAcceptanceDays
      maxAcceptanceSeverity: $maxAcceptanceSeverity
      maxNumberAcceptations: $maxNumberAcceptations
      minAcceptanceSeverity: $minAcceptanceSeverity
      organizationId: $organizationId
      organizationName: $organizationName
    ) {
      success
    }
  }
`;

export { GET_ORGANIZATION_POLICIES, UPDATE_ORGANIZATION_POLICIES };
