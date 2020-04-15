import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_ROLE: DocumentNode = gql`
  query GetRole($projectName: String!) {
    me {
      role(projectName: $projectName)
    }
  }
`;
