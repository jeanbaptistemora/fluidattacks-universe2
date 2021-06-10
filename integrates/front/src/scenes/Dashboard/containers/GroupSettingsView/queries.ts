import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_GROUP_DATA: DocumentNode = gql`
  query GetGroupData($groupName: String!) {
    group(groupName: $groupName) {
      hasDrills
      hasForces
      hasSkims
      language
      name
      subscription
    }
  }
`;

const EDIT_GROUP_DATA: DocumentNode = gql`
  mutation EditGroupData(
    $comments: String!
    $groupName: String!
    $hasDrills: Boolean!
    $hasForces: Boolean!
    $hasIntegrates: Boolean!
    $hasSkims: Boolean!
    $reason: EditGroupReason!
    $subscription: SubscriptionType!
  ) {
    editGroup(
      comments: $comments
      groupName: $groupName
      hasDrills: $hasDrills
      hasForces: $hasForces
      hasIntegrates: $hasIntegrates
      hasSkims: $hasSkims
      reason: $reason
      subscription: $subscription
    ) {
      success
    }
  }
`;

const REMOVE_TAG_MUTATION: DocumentNode = gql`
  mutation RemoveTagMutation($tagToRemove: String!, $projectName: String!) {
    removeTag(tag: $tagToRemove, projectName: $projectName) {
      success
    }
  }
`;

const GET_TAGS: DocumentNode = gql`
  query GetTagsQuery($projectName: String!) {
    group(groupName: $projectName) {
      name
      tags
    }
  }
`;

const ADD_TAGS_MUTATION: DocumentNode = gql`
  mutation AddTagsMutation($projectName: String!, $tagsData: JSONString!) {
    addTags(tags: $tagsData, projectName: $projectName) {
      success
    }
  }
`;

const UPDATE_ENVIRONMENT_MUTATION: DocumentNode = gql`
  mutation UpdateEnvironmentMutation(
    $groupName: String!
    $env: EnvironmentInput!
    $state: ResourceState!
  ) {
    updateEnvironment(projectName: $groupName, env: $env, state: $state) {
      success
    }
  }
`;

const ADD_ENVIRONMENTS_MUTATION: DocumentNode = gql`
  mutation AddEnvironmentsMutation(
    $groupName: String!
    $envs: [EnvironmentInput]!
  ) {
    addEnvironments(projectName: $groupName, envs: $envs) {
      success
    }
  }
`;

const GET_ENVIRONMENTS: DocumentNode = gql`
  query GetEnvironmentsQuery($groupName: String!) {
    resources(projectName: $groupName) {
      environments
    }
  }
`;

const GET_FILES: DocumentNode = gql`
  query GetFilesQuery($projectName: String!) {
    resources(projectName: $projectName) {
      files
    }
  }
`;

const DOWNLOAD_FILE_MUTATION: DocumentNode = gql`
  mutation DownloadFileMutation(
    $filesData: JSONString!
    $projectName: String!
  ) {
    downloadFile(filesData: $filesData, projectName: $projectName) {
      success
      url
    }
  }
`;

const REMOVE_FILE_MUTATION: DocumentNode = gql`
  mutation RemoveFileMutation($filesData: JSONString!, $projectName: String!) {
    removeFiles(filesData: $filesData, projectName: $projectName) {
      success
    }
  }
`;

const UPLOAD_FILE_MUTATION: DocumentNode = gql`
  mutation UploadFileMutation(
    $file: Upload!
    $filesData: JSONString!
    $projectName: String!
  ) {
    addFiles(file: $file, filesData: $filesData, projectName: $projectName) {
      success
    }
  }
`;

export {
  GET_GROUP_DATA,
  EDIT_GROUP_DATA,
  REMOVE_TAG_MUTATION,
  GET_TAGS,
  ADD_TAGS_MUTATION,
  UPDATE_ENVIRONMENT_MUTATION,
  ADD_ENVIRONMENTS_MUTATION,
  GET_ENVIRONMENTS,
  GET_FILES,
  DOWNLOAD_FILE_MUTATION,
  REMOVE_FILE_MUTATION,
  UPLOAD_FILE_MUTATION,
};
