import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_ORGANIZATION_SETTINGS: DocumentNode = gql`
  query OrganizationSettings ($organizationId: String!) {
    organization(organizationId: $organizationId) {
      maxAcceptanceDays
      maxAcceptanceSeverity
      maxNumberAcceptations
      minAcceptanceSeverity
    }
  }
  `;
