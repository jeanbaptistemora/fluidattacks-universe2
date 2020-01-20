import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_PROJECT_ALERT: DocumentNode = gql`
  query GetProjectAlert($projectName: String!, $organization: String!) {
    alert(projectName: $projectName, organization: $organization) {
      message
      status
    }
  }
`;
