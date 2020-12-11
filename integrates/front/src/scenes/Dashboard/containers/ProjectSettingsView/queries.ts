import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_GROUP_DATA: DocumentNode = gql`
  query GetGroupData($groupName: String!) {
    project(projectName: $groupName) {
      hasDrills
      hasForces
      subscription
    }
  }
  `;

export const EDIT_GROUP_DATA: DocumentNode = gql`
  mutation EditGroupData(
    $comments: String!
    $groupName: String!
    $hasDrills: Boolean!
    $hasForces: Boolean!
    $hasIntegrates: Boolean!
    $reason: EditGroupReason!
    $subscription: SubscriptionType!
  ) {
    editGroup(
      comments: $comments
      groupName: $groupName
      hasDrills: $hasDrills
      hasForces: $hasForces
      hasIntegrates: $hasIntegrates
      reason: $reason
      subscription: $subscription
    ) {
      success
    }
  }
  `;

export const REMOVE_TAG_MUTATION: DocumentNode = gql`
  mutation RemoveTagMutation($tagToRemove: String!, $projectName: String!) {
    removeTag (
      tag: $tagToRemove,
      projectName: $projectName,
    ) {
      success
    }
  }
  `;

export const GET_TAGS: DocumentNode = gql`
  query GetTagsQuery($projectName: String!) {
    project(projectName: $projectName){
      tags
    }
  }
  `;

export const ADD_TAGS_MUTATION: DocumentNode = gql`
  mutation AddTagsMutation($projectName: String!, $tagsData: JSONString!) {
    addTags (
      tags: $tagsData,
      projectName: $projectName) {
      success
    }
  }
  `;

export const UPDATE_ENVIRONMENT_MUTATION: DocumentNode = gql`
  mutation UpdateEnvironmentMutation($projectName: String!, $env: EnvironmentInput!, $state: ResourceState!) {
    updateEnvironment(projectName: $projectName, env: $env, state: $state) {
      success
    }
  }
`;

export const ADD_ENVIRONMENTS_MUTATION: DocumentNode = gql`
  mutation AddEnvironmentsMutation($projectName: String!, $envs: [EnvironmentInput]!) {
    addEnvironments(projectName: $projectName, envs: $envs) {
      success
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

export const GET_FILES: DocumentNode = gql`
  query GetFilesQuery($projectName: String!) {
    resources(projectName: $projectName) {
      files
    }
  }
`;

export const DOWNLOAD_FILE_MUTATION: DocumentNode = gql`
  mutation DownloadFileMutation($filesData: JSONString!, $projectName: String!) {
    downloadFile(filesData: $filesData, projectName: $projectName) {
      success
      url
    }
  }
`;

export const REMOVE_FILE_MUTATION: DocumentNode = gql`
  mutation RemoveFileMutation($filesData: JSONString!, $projectName: String!) {
    removeFiles(filesData: $filesData, projectName: $projectName) {
      success
    }
  }
`;

export const UPLOAD_FILE_MUTATION: DocumentNode = gql`
  mutation UploadFileMutation($file: Upload!, $filesData: JSONString!, $projectName: String!) {
    addFiles(file: $file, filesData: $filesData, projectName: $projectName) {
      success
    }
  }
`;
