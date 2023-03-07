import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const ADD_FINDING_MUTATION: DocumentNode = gql`
  mutation AddFindingMutation(
    $attackComplexity: Float!
    $attackVector: Float!
    $attackVectorDescription: String!
    $availabilityImpact: Float!
    $availabilityRequirement: Float!
    $confidentialityImpact: Float!
    $confidentialityRequirement: Float!
    $description: String!
    $exploitability: Float!
    $groupName: String!
    $integrityImpact: Float!
    $integrityRequirement: Float!
    $privilegesRequired: Float!
    $recommendation: String!
    $minTimeToRemediate: Int
    $modifiedAttackComplexity: Float!
    $modifiedAttackVector: Float!
    $modifiedAvailabilityImpact: Float!
    $modifiedConfidentialityImpact: Float!
    $modifiedIntegrityImpact: Float!
    $modifiedPrivilegesRequired: Float!
    $modifiedSeverityScope: Float!
    $modifiedUserInteraction: Float!
    $remediationLevel: Float!
    $reportConfidence: Float!
    $severityScope: Float!
    $threat: String!
    $title: String!
    $unfulfilledRequirements: [String!]!
    $userInteraction: Float!
  ) {
    addFinding(
      attackComplexity: $attackComplexity
      attackVector: $attackVector
      attackVectorDescription: $attackVectorDescription
      availabilityImpact: $availabilityImpact
      availabilityRequirement: $availabilityRequirement
      confidentialityImpact: $confidentialityImpact
      confidentialityRequirement: $confidentialityRequirement
      description: $description
      exploitability: $exploitability
      groupName: $groupName
      integrityImpact: $integrityImpact
      integrityRequirement: $integrityRequirement
      privilegesRequired: $privilegesRequired
      recommendation: $recommendation
      minTimeToRemediate: $minTimeToRemediate
      modifiedAttackComplexity: $modifiedAttackComplexity
      modifiedAttackVector: $modifiedAttackVector
      modifiedAvailabilityImpact: $modifiedAvailabilityImpact
      modifiedConfidentialityImpact: $modifiedConfidentialityImpact
      modifiedIntegrityImpact: $modifiedIntegrityImpact
      modifiedPrivilegesRequired: $modifiedPrivilegesRequired
      modifiedSeverityScope: $modifiedSeverityScope
      modifiedUserInteraction: $modifiedUserInteraction
      remediationLevel: $remediationLevel
      reportConfidence: $reportConfidence
      severityScope: $severityScope
      threat: $threat
      title: $title
      unfulfilledRequirements: $unfulfilledRequirements
      userInteraction: $userInteraction
    ) {
      success
    }
  }
`;

const GET_FINDINGS: DocumentNode = gql`
  query GetFindingsQuery($groupName: String!) {
    group(groupName: $groupName) {
      findings {
        id
        age
        closedVulnerabilities
        lastVulnerability
        title
        description
        severityScore
        openAge
        openVulnerabilities
        status
        minTimeToRemediate
        isExploitable
        releaseDate
        treatmentSummary {
          accepted
          acceptedUndefined
          inProgress
          untreated
        }
        verificationSummary {
          onHold
          requested
          verified
        }
        verified
      }
      name
      businessId
      businessName
      description
      hasMachine
      userRole
    }
  }
`;

const REQUEST_GROUP_REPORT: DocumentNode = gql`
  query RequestGroupReport(
    $age: Int
    $reportType: ReportType!
    $groupName: String!
    $lang: ReportLang
    $lastReport: Int
    $location: String
    $minReleaseDate: DateTime
    $maxReleaseDate: DateTime
    $treatments: [VulnerabilityTreatment!]
    $states: [VulnerabilityState!]
    $verifications: [VulnerabilityVerification!]
    $closingDate: DateTime
    $maxSeverity: Float
    $minSeverity: Float
    $findingTitle: String
    $verificationCode: String!
  ) {
    report(
      age: $age
      reportType: $reportType
      findingTitle: $findingTitle
      groupName: $groupName
      lang: $lang
      lastReport: $lastReport
      location: $location
      maxReleaseDate: $maxReleaseDate
      maxSeverity: $maxSeverity
      minReleaseDate: $minReleaseDate
      minSeverity: $minSeverity
      states: $states
      treatments: $treatments
      verifications: $verifications
      closingDate: $closingDate
      verificationCode: $verificationCode
    ) {
      success
    }
  }
`;

const GET_GROUP_VULNERABILITIES: DocumentNode = gql`
  query GetGroupVulnerabilities(
    $after: String
    $first: Int
    $groupName: String!
    $root: String
  ) {
    group(groupName: $groupName) {
      name
      vulnerabilities(after: $after, first: $first, root: $root) {
        edges {
          node {
            findingId
            id
            state
            treatmentAssigned
            where
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
      }
    }
  }
`;

const GET_ROOTS: DocumentNode = gql`
  query GetRoots($groupName: String!) {
    group(groupName: $groupName) {
      name
      roots {
        ... on GitRoot {
          id
          nickname
          state
        }
        ... on IPRoot {
          id
          nickname
          state
        }
        ... on URLRoot {
          id
          nickname
          state
        }
      }
    }
  }
`;

export {
  ADD_FINDING_MUTATION,
  GET_FINDINGS,
  GET_GROUP_VULNERABILITIES,
  REQUEST_GROUP_REPORT,
  GET_ROOTS,
};
