import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_USER: DocumentNode = gql`
  query GetUserDataQuery($projectName: String!, $userEmail: String!) {
    user(projectName: $projectName, userEmail: $userEmail) {
      organization
      responsibility
      phoneNumber
    }
  }
  `;
