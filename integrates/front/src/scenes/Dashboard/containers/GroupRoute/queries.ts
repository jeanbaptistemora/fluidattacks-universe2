import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_GROUP_DATA: DocumentNode = gql`
  query GetGroupDataQuery($groupName: String!) {
    group(groupName: $groupName) {
      deletionDate
      name
      organization
      serviceAttributes
    }
  }
`;
