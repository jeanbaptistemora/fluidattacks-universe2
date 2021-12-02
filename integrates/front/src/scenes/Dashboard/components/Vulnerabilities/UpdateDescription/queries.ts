import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const UPDATE_DESCRIPTION_MUTATION: DocumentNode = gql`
  mutation UpdateVulnerabilityTreatmentMutation(
    $findingId: String!
    $severity: Int
    $tag: String
    $treatmentManager: String
    $vulnerabilityId: ID!
    $externalBugTrackingSystem: String
    $acceptanceDate: String
    $justification: String!
    $treatment: UpdateClientDescriptionTreatment!
    $isVulnTreatmentChanged: Boolean!
    $isVulnInfoChanged: Boolean!
  ) {
    updateVulnerabilityTreatment(
      externalBugTrackingSystem: $externalBugTrackingSystem
      findingId: $findingId
      severity: $severity
      tag: $tag
      vulnerabilityId: $vulnerabilityId
    ) @include(if: $isVulnInfoChanged) {
      success
    }
    updateVulnerabilitiesTreatment(
      acceptanceDate: $acceptanceDate
      findingId: $findingId
      justification: $justification
      treatment: $treatment
      treatmentManager: $treatmentManager
      vulnerabilityId: $vulnerabilityId
    ) @include(if: $isVulnTreatmentChanged) {
      success
    }
  }
`;

const REMOVE_TAGS_MUTATION: DocumentNode = gql`
  mutation RemoveTagsVuln(
    $findingId: String!
    $tag: String
    $vulnerabilities: [String]!
  ) {
    removeTags(
      findingId: $findingId
      tag: $tag
      vulnerabilities: $vulnerabilities
    ) {
      success
    }
  }
`;

const REQUEST_VULNS_ZERO_RISK: DocumentNode = gql`
  mutation RequestVulnerabilitiesZeroRisk(
    $findingId: String!
    $justification: String!
    $vulnerabilities: [String]!
  ) {
    requestVulnerabilitiesZeroRisk(
      findingId: $findingId
      justification: $justification
      vulnerabilities: $vulnerabilities
    ) {
      success
    }
  }
`;

export {
  REMOVE_TAGS_MUTATION,
  REQUEST_VULNS_ZERO_RISK,
  UPDATE_DESCRIPTION_MUTATION,
};
