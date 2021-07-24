import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const ADD_ORGANIZATION_FINDING_POLICY: DocumentNode = gql`
  mutation AddOrganizationFindingPolicy(
    $name: String!
    $organizationName: String!
    $tags: [String]
  ) {
    addOrganizationFindingPolicy(
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
      groups {
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
  mutation DeactivateOrganizationFindingPolicy(
    $findingPolicyId: ID!
    $organizationName: String!
  ) {
    deactivateOrganizationFindingPolicy(
      findingPolicyId: $findingPolicyId
      organizationName: $organizationName
    ) {
      success
    }
  }
`;

const HANDLE_ORGANIZATION_FINDING_POLICY: DocumentNode = gql`
  mutation HandleOrganizationFindingPolicyAcceptation(
    $findingPolicyId: ID!
    $organizationName: String!
    $status: OrganizationFindindPolicy!
  ) {
    handleOrganizationFindingPolicyAcceptation(
      findingPolicyId: $findingPolicyId
      organizationName: $organizationName
      status: $status
    ) {
      success
    }
  }
`;

const RESUBMIT_ORGANIZATION_FINDING_POLICY: DocumentNode = gql`
  mutation SubmitOrganizationFindingPolicy(
    $organizationName: String!
    $findingPolicyId: ID!
  ) {
    submitOrganizationFindingPolicy(
      findingPolicyId: $findingPolicyId
      organizationName: $organizationName
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
  RESUBMIT_ORGANIZATION_FINDING_POLICY,
};
