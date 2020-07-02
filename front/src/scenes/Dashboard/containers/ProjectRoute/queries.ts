import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_GROUP_DATA: DocumentNode = gql`
  query GetProjectDataQuery($projectName: String!, $organization: String!) {
    alert(projectName: $projectName, organization: $organization) {
      message
      status
    }
    project(projectName: $projectName){
      deletionDate
      serviceAttributes
      userDeletion
    }
  }
`;

export const REJECT_REMOVE_PROJECT_MUTATION: DocumentNode = gql`
  mutation RejectProjectDeletion($projectName: String!) {
    rejectRemoveProject(projectName: $projectName) {
      success
    }
  }
`;

export const GET_GROUP_SERVICE_ATTRIBUTES: DocumentNode = gql`
  query GetGroupServiceAttributes($projectName: String!) {
    project(projectName: $projectName) {
      serviceAttributes
    }
  }
`;
