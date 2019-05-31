import { gql } from "apollo-boost";
import { DocumentNode } from "graphql";

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

export const REMOVE_REPO_MUTATION: DocumentNode = gql`
  mutation RemoveRepoMutation($projectName: String!, $repoData: JSONString!, ) {
    removeRepositories (
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
