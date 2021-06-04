import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const ADD_ORGANIZATION_FINDING_POLICY: DocumentNode = gql`
  mutation AddOrgFindingPolicy(
    $name: String!
    $organizationName: String!
    $tags: [String]
  ) {
    addOrgFindingPolicy(
      findingName: $name
      organizationName: $organizationName
      tags: $tags
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

const DEACTIVATE_ORGANIZATION_FINDING_POLICY: DocumentNode = gql`
  mutation DeactivateOrgFindingPolicy(
    $findingPolicyId: ID!
    $organizationName: String!
  ) {
    deactivateOrgFindingPolicy(
      findingPolicyId: $findingPolicyId
      organizationName: $organizationName
    ) {
      success
    }
  }
`;

const HANDLE_ORGANIZATION_FINDING_POLICY: DocumentNode = gql`
  mutation HandleOrgFindingPolicyAcceptation(
    $findingPolicyId: ID!
    $organizationName: String!
    $status: OrganizationFindindPolicy!
  ) {
    handleOrgFindingPolicyAcceptation(
      findingPolicyId: $findingPolicyId
      organizationName: $organizationName
      status: $status
    ) {
      success
    }
  }
`;

export {
  ADD_ORGANIZATION_FINDING_POLICY,
  GET_ORGANIZATION_FINDINGS_TITLES,
  DEACTIVATE_ORGANIZATION_FINDING_POLICY,
  HANDLE_ORGANIZATION_FINDING_POLICY,
};
