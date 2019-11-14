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

export const UPDATE_REPO_MUTATION: DocumentNode = gql`
  mutation UpdateRepoMutation($projectName: String!, $repoData: JSONString!, ) {
    updateRepositories (
      repositoryData: $repoData,
      projectName: $projectName
    ) {
      success
      resources {
        repositories
      }
    }
  }
  `;

export const ADD_REPOS_MUTATION: DocumentNode = gql`
  mutation AddReposMutation($projectName: String!, $repoData: JSONString!) {
    addRepositories (
      resourcesData: $repoData,
      projectName: $projectName) {
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
}
`;

export const REMOVE_ENV_MUTATION: DocumentNode = gql`
  mutation RemoveEnvMutation($projectName: String!, $envData: JSONString!, ) {
    removeEnvironments (
      repositoryData: $envData,
      projectName: $projectName
    ) {
      success
      resources {
        environments
      }
    }
  }
  `;

export const ADD_ENVS_MUTATION: DocumentNode = gql`
  mutation AddEnvsMutation($projectName: String!, $envData: JSONString!) {
    addEnvironments (
      resourcesData: $envData,
      projectName: $projectName) {
      success
      resources {
        repositories
      }
    }
  }
  `;
