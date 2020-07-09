import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_ORGANIZATION_POLICIES: DocumentNode = gql`
  query GetOrganizationPolicies ($organizationId: String!) {
    organization(organizationId: $organizationId) {
      maxAcceptanceDays
      maxAcceptanceSeverity
      maxNumberAcceptations
      minAcceptanceSeverity
    }
  }
  `;

export const UPDATE_ORGANIZATION_POLICIES: DocumentNode = gql`
  mutation UpdateOrganizationPolicies(
    $maxAcceptanceDays: Int,
    $maxAcceptanceSeverity: Float,
    $maxNumberAcceptations: Int,
    $minAcceptanceSeverity: Float
    $organizationId: String!
    $organizationName: String!
  ) {
    updateOrganizationPolicies(
      maxAcceptanceDays: $maxAcceptanceDays,
      maxAcceptanceSeverity: $maxAcceptanceSeverity,
      maxNumberAcceptations: $maxNumberAcceptations,
      minAcceptanceSeverity: $minAcceptanceSeverity,
      organizationId: $organizationId,
      organizationName: $organizationName
    ) {
      success
    }
  }
  `;
