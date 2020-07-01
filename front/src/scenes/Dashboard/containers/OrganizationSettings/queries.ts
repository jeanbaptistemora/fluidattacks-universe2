import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_ORGANIZATION_ID: DocumentNode = gql`
query GetOrganizationId ($organizationName: String!) {
  organizationId(organizationName: $organizationName) {
    id
  }
}
`;

export const GET_ORGANIZATION_SETTINGS: DocumentNode = gql`
  query GetOrganizationSettings ($organizationId: String!) {
    organization(organizationId: $organizationId) {
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
    $organizationId: String!
    $organizationName: String!
  ) {
    updateOrganizationSettings(
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
