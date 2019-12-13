import { DocumentNode } from "graphql";
import gql from "graphql-tag";

const FRAGMENTS: Dictionary<DocumentNode> = {
  commentFields: gql`
    fragment commentFields on Comment {
      id
      content
      created
      email
      fullname
      modified
      parent
    }
  `,
};

export const GET_FINDING_COMMENTS: DocumentNode = gql`
  query GetFindingComments($findingId: String!) {
    finding(identifier: $findingId) {
      comments {
        ...commentFields
      }
      id
    }
  }
  ${FRAGMENTS.commentFields}
`;

export const GET_FINDING_OBSERVATIONS: DocumentNode = gql`
  query GetFindingObservations($findingId: String!) {
    finding(identifier: $findingId) {
      observations {
        ...commentFields
      }
      id
    }
  }
  ${FRAGMENTS.commentFields}
`;

export const ADD_FINDING_COMMENT: DocumentNode = gql`
  mutation AddFindingComment($content: String!, $findingId: String!, $parent: String!, $type: String!) {
    addFindingComment(content: $content, findingId: $findingId, parent: $parent, type: $type) {
      commentId
      success
    }
  }
`;
