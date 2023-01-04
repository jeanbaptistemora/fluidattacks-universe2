import { DocumentNode, gql } from "@apollo/client/core";

const GET_GROUPS: DocumentNode = gql`
  query GetGroups {
    me {
      userEmail
      organizations {
        groups {
          name
          subscription
        }
      }
    }
  }
`;

const GET_GIT_ROOTS = gql`
  query MeltsGetGitRoots($groupName: String!) {
    group(groupName: $groupName) {
      roots {
        ... on GitRoot {
          nickname
          downloadUrl
        }
      }
    }
  }
`;
export { GET_GROUPS, GET_GIT_ROOTS };
