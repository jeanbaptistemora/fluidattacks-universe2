import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_VULNERABILITIES: DocumentNode = gql`
  query GetVulnerabilitiesQuery($identifier: String!, $analystField: Boolean!) {
    finding(identifier: $identifier) {
      btsUrl
      id
      releaseDate
      portsVulns {
        ...vulnInfo
        analyst @include(if: $analystField)
      }
      linesVulns {
        ...vulnInfo
        analyst @include(if: $analystField)
      }
      inputsVulns {
        ...vulnInfo
        analyst @include(if: $analystField)
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
    remediated
    verification
  }
  `;

export const UPDATE_TREATMENT_MUTATION: DocumentNode = gql`
  mutation UpdateTreatmentVulnMutation(
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

export const UPLOAD_VULNERABILITIES: DocumentNode = gql`
  mutation UploadVulnerabilites ($file: Upload!, $findingId: String!){
    uploadFile(findingId: $findingId, file: $file) {
      success
    }
  }`
;

export const DELETE_TAGS_MUTATION: DocumentNode = gql`
  mutation DeleteTagsVuln ($findingId: String!, $tag: String, $vulnerabilities: [String]!){
    deleteTags(findingId: $findingId, tag: $tag, vulnerabilities: $vulnerabilities) {
      success
    }
  }`
;

export const GET_PROJECT_USERS: DocumentNode = gql`
  query GetProjectUsers($projectName: String!) {
    project(projectName: $projectName) {
      stakeholders {
        email
      }
    }
  }
`;

export const DOWNLOAD_VULNERABILITIES: DocumentNode = gql`
  mutation downloadVulnFile($findingId: String!) {
    downloadVulnFile(findingId: $findingId) {
      success
      url
    }
  }
`;
