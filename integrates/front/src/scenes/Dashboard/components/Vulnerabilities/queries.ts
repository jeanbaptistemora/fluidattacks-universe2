import { DocumentNode } from "graphql";
import gql from "graphql-tag";

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
