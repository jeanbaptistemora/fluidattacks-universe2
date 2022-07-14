import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_GROUP_POLICIES: DocumentNode = gql`
  query GetGroupPolicies($groupName: String!) {
    group(groupName: $groupName) {
      maxAcceptanceDays
      maxAcceptanceSeverity
      maxNumberAcceptances
      minAcceptanceSeverity
      minBreakingSeverity
      vulnerabilityGracePeriod
      name
    }
  }
`;

const UPDATE_GROUP_POLICIES: DocumentNode = gql`
  mutation UpdateGroupPolicies(
    $groupName: String!
    $maxAcceptanceDays: Int
    $maxAcceptanceSeverity: Float
    $maxNumberAcceptances: Int
    $minAcceptanceSeverity: Float
    $minBreakingSeverity: Float
    $vulnerabilityGracePeriod: Int
  ) {
    updateGroupPolicies(
      groupName: $groupName
      maxAcceptanceDays: $maxAcceptanceDays
      maxAcceptanceSeverity: $maxAcceptanceSeverity
      maxNumberAcceptances: $maxNumberAcceptances
      minBreakingSeverity: $minBreakingSeverity
      minAcceptanceSeverity: $minAcceptanceSeverity
      vulnerabilityGracePeriod: $vulnerabilityGracePeriod
    ) {
      success
    }
  }
`;

export { GET_GROUP_POLICIES, UPDATE_GROUP_POLICIES };
