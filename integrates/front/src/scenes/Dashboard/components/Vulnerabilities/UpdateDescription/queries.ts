import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const UPDATE_DESCRIPTION_MUTATION: DocumentNode = gql`
  mutation UpdateVulnerabilityTreatmentMutation(
    $findingId: String!
    $severity: Int
    $tag: String
    $treatmentManager: String
    $vulnerabilityId: ID!
    $externalBts: String!
    $acceptanceDate: String
    $justification: String!
    $treatment: UpdateClientDescriptionTreatment!
    $isVulnTreatmentChanged: Boolean!
    $isVulnInfoChanged: Boolean!
  ) {
    updateVulnerabilityTreatment(
      externalBts: $externalBts
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

const REQUEST_ZERO_RISK_VULN: DocumentNode = gql`
  mutation RequestZeroRiskVulnerabilities(
    $findingId: String!
    $justification: String!
    $vulnerabilities: [String]!
  ) {
    requestZeroRiskVulnerabilities(
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
  REQUEST_ZERO_RISK_VULN,
  UPDATE_DESCRIPTION_MUTATION,
};
