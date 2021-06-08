import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const UPLOAD_VULNERABILITIES: DocumentNode = gql`
  mutation UploadVulnerabilites($file: Upload!, $findingId: String!) {
    uploadFile(findingId: $findingId, file: $file) {
      success
    }
  }
`;

const GET_GROUP_USERS: DocumentNode = gql`
  query GetProjectUsers($projectName: String!) {
    group(groupName: $projectName) {
      name
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

export { DOWNLOAD_VULNERABILITIES, GET_GROUP_USERS, UPLOAD_VULNERABILITIES };
