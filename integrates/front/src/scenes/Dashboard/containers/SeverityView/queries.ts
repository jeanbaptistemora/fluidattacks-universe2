import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_SEVERITY: DocumentNode = gql`
  query GetSeverityQuery($identifier: String!) {
    finding(identifier: $identifier) {
      id
      cvssVersion
      severityScore
      severity {
        attackComplexity
        attackVector
        availabilityImpact
        availabilityRequirement
        confidentialityImpact
        confidentialityRequirement
        exploitability
        integrityImpact
        integrityRequirement
        modifiedAttackComplexity
        modifiedAttackVector
        modifiedAvailabilityImpact
        modifiedConfidentialityImpact
        modifiedIntegrityImpact
        modifiedPrivilegesRequired
        modifiedSeverityScope
        modifiedUserInteraction
        privilegesRequired
        remediationLevel
        reportConfidence
        severityScope
        userInteraction
      }
    }
  }
`;

const UPDATE_SEVERITY_MUTATION: DocumentNode = gql`
  mutation UpdateSeverityMutation(
    $findingId: String!
    $attackComplexity: String!
    $attackVector: String!
    $availabilityImpact: String!
    $availabilityRequirement: String!
    $confidentialityImpact: String!
    $confidentialityRequirement: String!
    $cvssVersion: String!
    $exploitability: String!
    $integrityImpact: String!
    $integrityRequirement: String!
    $modifiedAttackComplexity: String!
    $modifiedAttackVector: String!
    $modifiedAvailabilityImpact: String!
    $modifiedConfidentialityImpact: String!
    $modifiedIntegrityImpact: String!
    $modifiedPrivilegesRequired: String!
    $modifiedSeverityScope: String!
    $modifiedUserInteraction: String!
    $privilegesRequired: String!
    $remediationLevel: String!
    $reportConfidence: String!
    $severity: String
    $severityScope: String!
    $userInteraction: String!
  ) {
    updateSeverity(
      findingId: $findingId
      attackComplexity: $attackComplexity
      attackVector: $attackVector
      availabilityImpact: $availabilityImpact
      availabilityRequirement: $availabilityRequirement
      confidentialityImpact: $confidentialityImpact
      confidentialityRequirement: $confidentialityRequirement
      cvssVersion: $cvssVersion
      exploitability: $exploitability
      integrityImpact: $integrityImpact
      integrityRequirement: $integrityRequirement
      modifiedAttackComplexity: $modifiedAttackComplexity
      modifiedAttackVector: $modifiedAttackVector
      modifiedAvailabilityImpact: $modifiedAvailabilityImpact
      modifiedConfidentialityImpact: $modifiedConfidentialityImpact
      modifiedIntegrityImpact: $modifiedIntegrityImpact
      modifiedPrivilegesRequired: $modifiedPrivilegesRequired
      modifiedSeverityScope: $modifiedSeverityScope
      modifiedUserInteraction: $modifiedUserInteraction
      privilegesRequired: $privilegesRequired
      remediationLevel: $remediationLevel
      reportConfidence: $reportConfidence
      severity: $severity
      severityScope: $severityScope
      userInteraction: $userInteraction
    ) {
      success
      finding {
        cvssVersion
        severity
      }
    }
  }
`;

export { GET_SEVERITY, UPDATE_SEVERITY_MUTATION };
