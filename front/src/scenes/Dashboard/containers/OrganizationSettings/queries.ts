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
    $identifier: String!
    $maxAcceptanceDays: Int,
    $maxAcceptanceSeverity: Float!,
    $maxNumberAcceptations: Int,
    $minAcceptanceSeverity: Float!
  ) {
    updateOrganizationSettings(
      identifier: $identifier
      maxAcceptanceDays: $maxAcceptanceDays,
      maxAcceptanceSeverity: $maxAcceptanceSeverity,
      maxNumberAcceptations: $maxNumberAcceptations,
      minAcceptanceSeverity: $minAcceptanceSeverity
    ) {
      success
    }
  }
  `;
