import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_GROUP_DATA: DocumentNode = gql`
  query GetGroupData($groupName: String!) {
    group(groupName: $groupName) {
      description
      hasSquad
      hasMachine
      language
      name
      service
      subscription
    }
  }
`;

const UPDATE_GROUP_DATA: DocumentNode = gql`
  mutation UpdateGroupData(
    $comments: String!
    $description: String
    $groupName: String!
    $hasASM: Boolean!
    $hasMachine: Boolean!
    $hasSquad: Boolean!
    $language: String
    $reason: UpdateGroupReason!
    $service: ServiceType!
    $subscription: SubscriptionType!
  ) {
    updateGroup(
      comments: $comments
      description: $description
      groupName: $groupName
      hasSquad: $hasSquad
      hasAsm: $hasASM
      hasMachine: $hasMachine
      language: $language
      reason: $reason
      service: $service
      subscription: $subscription
    ) {
      success
    }
  }
`;

const REMOVE_GROUP_TAG_MUTATION: DocumentNode = gql`
  mutation RemoveGroupTagMutation($tagToRemove: String!, $groupName: String!) {
    removeGroupTag(tag: $tagToRemove, groupName: $groupName) {
      success
    }
  }
`;

const GET_TAGS: DocumentNode = gql`
  query GetTagsQuery($groupName: String!) {
    group(groupName: $groupName) {
      name
      tags
    }
  }
`;

const ADD_GROUP_TAGS_MUTATION: DocumentNode = gql`
  mutation AddGroupTagsMutation($groupName: String!, $tagsData: JSONString!) {
    addGroupTags(tags: $tagsData, groupName: $groupName) {
      success
    }
  }
`;

const GET_FILES: DocumentNode = gql`
  query GetFilesQuery($groupName: String!) {
    resources(groupName: $groupName) {
      files
    }
  }
`;

const DOWNLOAD_FILE_MUTATION: DocumentNode = gql`
  mutation DownloadFileMutation($filesData: JSONString!, $groupName: String!) {
    downloadFile(filesData: $filesData, groupName: $groupName) {
      success
      url
    }
  }
`;

const REMOVE_FILE_MUTATION: DocumentNode = gql`
  mutation RemoveFileMutation($filesData: JSONString!, $groupName: String!) {
    removeFiles(filesData: $filesData, groupName: $groupName) {
      success
    }
  }
`;

const SIGN_POST_URL_MUTATION: DocumentNode = gql`
  mutation SignPostUrlMutation($filesData: JSONString!, $groupName: String!) {
    signPostUrl(filesData: $filesData, groupName: $groupName) {
      success
      url {
        url
        fields {
          key
          awsaccesskeyid
          policy
          signature
        }
      }
    }
  }
`;

const ADD_FILES_TO_DB_MUTATION: DocumentNode = gql`
  mutation addFilesToDbMutation($filesData: JSONString!, $groupName: String!) {
    addFilesToDb(filesData: $filesData, groupName: $groupName) {
      success
    }
  }
`;

export {
  GET_GROUP_DATA,
  UPDATE_GROUP_DATA,
  REMOVE_GROUP_TAG_MUTATION,
  GET_TAGS,
  ADD_GROUP_TAGS_MUTATION,
  GET_FILES,
  DOWNLOAD_FILE_MUTATION,
  REMOVE_FILE_MUTATION,
  SIGN_POST_URL_MUTATION,
  ADD_FILES_TO_DB_MUTATION,
};
