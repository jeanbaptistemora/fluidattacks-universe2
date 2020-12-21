import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_GROUP_DATA: DocumentNode = gql`
  query GetProjectDataQuery($projectName: String!) {
    project(projectName: $projectName){
      deletionDate
      serviceAttributes
      userDeletion
    }
  }
`;
