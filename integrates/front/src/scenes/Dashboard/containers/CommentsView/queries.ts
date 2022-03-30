import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const FRAGMENTS: Dictionary<DocumentNode> = {
  commentFields: gql`
    fragment commentFields on Consult {
      id
      content
      created
      email
      fullName
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
      fullName
      modified
      parent
    }
  `,
};

const GET_FINDING_CONSULTING: DocumentNode = gql`
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

const GET_FINDING_OBSERVATIONS: DocumentNode = gql`
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

const ADD_FINDING_CONSULT: DocumentNode = gql`
  mutation AddFindingConsult(
    $content: String!
    $findingId: String!
    $parent: GenericScalar!
    $type: FindingConsultType!
  ) {
    addFindingConsult(
      content: $content
      findingId: $findingId
      parentComment: $parent
      type: $type
    ) {
      commentId
      success
    }
  }
`;

export {
  GET_FINDING_CONSULTING,
  GET_FINDING_OBSERVATIONS,
  ADD_FINDING_CONSULT,
};
