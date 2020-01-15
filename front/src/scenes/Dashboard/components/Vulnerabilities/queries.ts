import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_VULNERABILITIES: DocumentNode = gql`
  query GetVulnerabilitiesQuery($identifier: String!, $analystField: Boolean!) {
    finding(identifier: $identifier) {
      id
      releaseDate
      portsVulns: vulnerabilities(
        vulnType: "ports") {
        ...vulnInfo
        lastAnalyst @include(if: $analystField)
      }
      linesVulns: vulnerabilities(
        vulnType: "lines") {
        ...vulnInfo
        lastAnalyst @include(if: $analystField)
      }
      pendingVulns: vulnerabilities(
        approvalStatus: "PENDING") {
        ...vulnInfo
        analyst @include(if: $analystField)
      }
      inputsVulns: vulnerabilities(
        vulnType: "inputs") {
        ...vulnInfo
        lastAnalyst @include(if: $analystField)
      }
    }
  }
  fragment vulnInfo on Vulnerability {
    vulnType
    where
    specific
    currentState
    id
    findingId
    acceptanceDate
    severity
    tag
    treatment
    treatmentManager
    treatmentJustification
    externalBts
    currentApprovalStatus
    lastApprovedStatus
  }
  `;

export const UPDATE_TREATMENT_MUTATION: DocumentNode = gql`
  mutation UpdateTreatmentMutation($acceptanceDate: String, $btsUrl: String, $findingId: String!, $treatment: String,
    $treatmentManager: String, $treatmentJustification: String, $vulnerabilities: [String]!, $severity: Int,
    $tag: String ) {
    updateTreatmentVuln (
      acceptanceDate: $acceptanceDate,
      btsUrl: $btsUrl,
      findingId: $findingId,
      treatment: $treatment,
      treatmentManager: $treatmentManager,
      treatmentJustification: $treatmentJustification,
      vulnerabilities: $vulnerabilities,
      severity: $severity,
      tag: $tag,
    ) {
      success
    }
  }
  `;

export const APPROVE_VULN_MUTATION: DocumentNode = gql`
  mutation ApproveVulnMutation($uuid: String, $findingId: String!, $approvalStatus: Boolean!) {
    approveVulnerability (
      findingId: $findingId,
      approvalStatus: $approvalStatus,
      uuid: $uuid
    ) {
      success
    }
  }
  `;

export const UPLOAD_VULNERABILITIES: DocumentNode = gql`
mutation UploadVulnerabilites ($file: Upload!, $findingId: String!){
  uploadFile(findingId: $findingId, file: $file) {
    success
  }
}`;

export const DELETE_TAGS_MUTATION: DocumentNode = gql`
mutation DeleteTagsVuln ($findingId: String!, $vulnerabilities: [String]!){
  deleteTags(findingId: $findingId, vulnerabilities: $vulnerabilities) {
    success
  }
}`;
