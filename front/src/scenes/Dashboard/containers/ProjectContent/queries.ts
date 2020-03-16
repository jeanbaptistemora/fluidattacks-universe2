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

export const GET_ROLE: DocumentNode = gql`
  query GetRole($projectName: String!) {
    me {
      role(projectName: $projectName)
    }
  }
`;
