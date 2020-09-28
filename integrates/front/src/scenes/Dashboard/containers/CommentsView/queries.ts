import { DocumentNode } from "graphql";
import gql from "graphql-tag";

const FRAGMENTS: Dictionary<DocumentNode> = {
  commentFields: gql`
    fragment commentFields on Consult {
      id
      content
      created
      email
      fullname
      modified
      parent
    }
  `,
  consultFields: gql`
    fragment consultFields on Consult {
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

export const GET_FINDING_CONSULTING: DocumentNode = gql`
  query GetFindingConsulting($findingId: String!) {
    finding(identifier: $findingId) {
      consulting {
        ...consultFields
      }
      id
    }
  }
  ${FRAGMENTS.consultFields}
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

export const ADD_FINDING_CONSULT: DocumentNode = gql`
  mutation AddFindingConsult(
      $content: String!, $findingId: String!, $parent: GenericScalar!, $type: FindingConsultType!) {
    addFindingConsult(content: $content, findingId: $findingId, parent: $parent, type: $type) {
      commentId
      success
    }
  }
`;
