import type { DocumentNode } from "graphql";
import gql from "graphql-tag";

const UPLOAD_VULNERABILITIES: DocumentNode = gql`
  mutation UploadVulnerabilites($file: Upload!, $findingId: String!) {
    uploadFile(findingId: $findingId, file: $file) {
      success
    }
  }
`;

const GET_PROJECT_USERS: DocumentNode = gql`
  query GetProjectUsers($projectName: String!) {
    project(projectName: $projectName) {
      stakeholders {
        email
      }
    }
  }
`;

const DOWNLOAD_VULNERABILITIES: DocumentNode = gql`
  mutation downloadVulnFile($findingId: String!) {
    downloadVulnFile(findingId: $findingId) {
      success
      url
    }
  }
`;

export { DOWNLOAD_VULNERABILITIES, GET_PROJECT_USERS, UPLOAD_VULNERABILITIES };
