import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_PROJECT_ORGANIZATION: DocumentNode = gql`
  query GetProjectOrganization ($projectName: String!) {
    project (projectName: $projectName) {
      organization
    }
  }
`;
