import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_VULNERABILITIES: DocumentNode = gql`
  query GetVulnerabilitiesQuery($identifier: String!, $analystField: Boolean!) {
    finding(identifier: $identifier) {
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
    historicTreatment {
      acceptanceDate
      acceptanceStatus
      date
      justification
      user
      treatment
      treatmentManager
    }
    id
    externalBts
    findingId
    severity
    tag
    treatmentManager
    remediated
    verification
    zeroRisk
  }
  `;

export const UPLOAD_VULNERABILITIES: DocumentNode = gql`
  mutation UploadVulnerabilites ($file: Upload!, $findingId: String!){
    uploadFile(findingId: $findingId, file: $file) {
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
