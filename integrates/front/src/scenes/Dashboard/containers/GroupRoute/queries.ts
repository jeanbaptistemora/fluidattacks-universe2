import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_GROUP_DATA: DocumentNode = gql`
  query GetProjectDataQuery($groupName: String!) {
    group(groupName: $groupName) {
      deletionDate
      name
      organization
      serviceAttributes
      userDeletion
    }
  }
`;
