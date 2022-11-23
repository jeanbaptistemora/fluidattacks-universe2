import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_ORGANIZATION_COMPLIANCE: DocumentNode = gql`
  query GetOrganizationCompliance($organizationId: String!) {
    organization(organizationId: $organizationId) {
      __typename
      name
      compliance {
        complianceLevel
        complianceWeeklyTrend
        estimatedDaysToFullCompliance
        standards {
          avgOrganizationComplianceLevel
          bestOrganizationComplianceLevel
          complianceLevel
          standardTitle
          worstOrganizationComplianceLevel
        }
      }
    }
  }
`;

export { GET_ORGANIZATION_COMPLIANCE };
