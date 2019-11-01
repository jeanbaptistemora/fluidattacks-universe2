import { gql } from "apollo-boost";
import { DocumentNode } from "graphql";

export const GET_USERS: DocumentNode = gql`
  query GetUserDataQuery($projectName: String!, $userEmail: String!) {
    user(projectName: $projectName, userEmail: $userEmail) {
      organization
      responsibility
      phoneNumber
    }
  }
  `;
