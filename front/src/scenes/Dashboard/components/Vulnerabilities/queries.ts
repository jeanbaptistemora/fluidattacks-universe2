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
    severity
    tag
    treatmentManager
    currentApprovalStatus
    lastApprovedStatus
    remediated
    verification
  }
  `;

export const UPDATE_TREATMENT_MUTATION: DocumentNode = gql`
  mutation UpdateTreatmentMutation(
    $findingId: String!,
    $severity: Int,
    $tag: String
    $treatmentManager: String,
    $vulnerabilities: [String]!,
  ) {
    updateTreatmentVuln (
      findingId: $findingId,
      severity: $severity,
      tag: $tag,
      treatmentManager: $treatmentManager,
      vulnerabilities: $vulnerabilities,
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

export const GET_PROJECT_USERS: DocumentNode = gql`
  query GetProjectUsers($projectName: String!) {
    project(projectName: $projectName) {
      users {
        email
      }
    }
  }
`;
