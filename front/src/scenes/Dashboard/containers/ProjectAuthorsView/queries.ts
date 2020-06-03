import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_BILL: DocumentNode = gql`
  query GetBill($projectName: String!) {
    project(projectName: $projectName) {
      bill {
        developers {
          actor
          commit
          groups
          organization
          repository
        }
      }
    }
  }
`;
