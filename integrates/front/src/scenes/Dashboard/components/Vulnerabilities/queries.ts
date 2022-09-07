/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const UPLOAD_VULNERABILITIES: DocumentNode = gql`
  mutation UploadVulnerabilities($file: Upload!, $findingId: String!) {
    uploadFile(findingId: $findingId, file: $file) {
      success
    }
  }
`;

const GET_GROUP_USERS: DocumentNode = gql`
  query GetGroupUsers($groupName: String!) {
    group(groupName: $groupName) {
      name
      stakeholders {
        email
        invitationState
      }
    }
  }
`;

const DOWNLOAD_VULNERABILITIES: DocumentNode = gql`
  mutation downloadVulnerabilityFile($findingId: String!) {
    downloadVulnerabilityFile(findingId: $findingId) {
      success
      url
    }
  }
`;

export { DOWNLOAD_VULNERABILITIES, GET_GROUP_USERS, UPLOAD_VULNERABILITIES };
