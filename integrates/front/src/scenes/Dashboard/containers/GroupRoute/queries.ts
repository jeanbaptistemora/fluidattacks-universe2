import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_GROUP_DATA: DocumentNode = gql`
  query GetProjectDataQuery($projectName: String!) {
    group(projectName: $projectName) {
      deletionDate
      name
      organization
      serviceAttributes
      userDeletion
    }
  }
`;
