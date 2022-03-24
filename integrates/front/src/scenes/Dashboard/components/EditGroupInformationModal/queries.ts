import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const UPDATE_GROUP_INFO: DocumentNode = gql`
  mutation UpdateGroupInfo(
    $businessId: String
    $businessName: String
    $description: String!
    $groupName: String!
    $language: Language!
  ) {
    updateGroupInfo(
      businessId: $businessId
      businessName: $businessName
      description: $description
      groupName: $groupName
      language: $language
    ) {
      success
    }
  }
`;

export { UPDATE_GROUP_INFO };
