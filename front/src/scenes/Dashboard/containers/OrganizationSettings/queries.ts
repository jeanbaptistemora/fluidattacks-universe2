import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_ORGANIZATION_SETTINGS: DocumentNode = gql`
  query GetOrganizationSettings ($identifier: String!) {
    organization(identifier: $identifier) {
      maxAcceptanceDays
      maxAcceptanceSeverity
      maxNumberAcceptations
      minAcceptanceSeverity
    }
  }
  `;

export const UPDATE_ORGANIZATION_SETTINGS: DocumentNode = gql`
  mutation UpdateOrganizationSettings(
    $maxAcceptanceDays: Int,
    $maxAcceptanceSeverity: Float!,
    $maxNumberAcceptations: Int,
    $minAcceptanceSeverity: Float!
    $organizationId: String!,
    $organizationName: String!,
  ) {
    updateOrganizationSettings(
      maxAcceptanceDays: $maxAcceptanceDays,
      maxAcceptanceSeverity: $maxAcceptanceSeverity,
      maxNumberAcceptations: $maxNumberAcceptations,
      minAcceptanceSeverity: $minAcceptanceSeverity
      organizationId: $organizationId,
      organizationName: $organizationName,
    ) {
      success
    }
  }
  `;
