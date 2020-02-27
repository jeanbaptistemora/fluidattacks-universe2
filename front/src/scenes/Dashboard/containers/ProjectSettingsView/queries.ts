import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const REMOVE_TAG_MUTATION: DocumentNode = gql`
  mutation RemoveTagMutation($tagToRemove: String!, $projectName: String!) {
    removeTag (
      tag: $tagToRemove,
      projectName: $projectName,
    ) {
      success
      project {
        deletionDate
        subscription
        tags
        name
      }
    }
  }
  `;

export const GET_TAGS: DocumentNode = gql`
  query GetTagsQuery($projectName: String!) {
    project(projectName: $projectName){
      deletionDate
      subscription
      tags
      name
    }
  }
  `;

export const ADD_TAGS_MUTATION: DocumentNode = gql`
  mutation AddTagsMutation($projectName: String!, $tagsData: JSONString!) {
    addTags (
      tags: $tagsData,
      projectName: $projectName) {
      success
      project {
        deletionDate
        name
        subscription
        tags
      }
    }
  }
  `;

export const GET_REPOSITORIES: DocumentNode = gql`
  query GetRepositoriesQuery($projectName: String!) {
    resources (projectName: $projectName) {
      repositories
    }
  }
  `;

export const UPDATE_RESOURCE_MUTATION: DocumentNode = gql`
  mutation UpdateResourceMutation($projectName: String!, $resData: JSONString!, $resType: String!) {
    updateResources (
      resourceData: $resData,
      projectName: $projectName,
      resType: $resType) {
      success
      resources {
        repositories
      }
    }
  }
  `;

export const ADD_RESOURCE_MUTATION: DocumentNode = gql`
  mutation AddResourceMutation($projectName: String!, $resData: JSONString!, $resType: String!) {
    addResources (
      resourceData: $resData,
      projectName: $projectName,
      resType: $resType) {
      success
      resources {
        repositories
      }
    }
  }
  `;

export const GET_ENVIRONMENTS: DocumentNode = gql`
query GetEnvironmentsQuery($projectName: String!) {
  resources (projectName: $projectName) {
    environments
  }
  project(projectName: $projectName){
    deletionDate
  }
}
`;

export const GET_PROJECT_DATA: DocumentNode = gql`
  query GetProjectDataQuery($projectName: String!) {
    project(projectName: $projectName){
      deletionDate
    }
  }
`;
