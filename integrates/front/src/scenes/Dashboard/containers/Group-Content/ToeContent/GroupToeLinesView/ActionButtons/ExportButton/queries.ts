import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const REQUEST_GROUP_TOE_LINES: DocumentNode = gql`
  query RequestGroupToeLines($groupName: String!, $verificationCode: String!) {
    toeLinesReport(groupName: $groupName, verificationCode: $verificationCode) {
      success
    }
  }
`;

export { REQUEST_GROUP_TOE_LINES };
