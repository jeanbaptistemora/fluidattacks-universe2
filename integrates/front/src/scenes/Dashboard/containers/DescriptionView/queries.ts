import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FINDING_DESCRIPTION: DocumentNode = gql`
  query GetFindingDescription(
    $canRetrieveHacker: Boolean!
    $canRetrieveSorts: Boolean!
    $findingId: String!
  ) {
    finding(identifier: $findingId) {
      affectedSystems
      attackVectorDescription
      compromisedAttributes
      compromisedRecords
      description
      hacker @include(if: $canRetrieveHacker)
      id
      openVulnerabilities
      recommendation
      requirements
      sorts @include(if: $canRetrieveSorts)
      state
      threat
      title
      type
    }
  }
`;

const UPDATE_DESCRIPTION_MUTATION: DocumentNode = gql`
  mutation UpdateFindingDescription(
    $affectedSystems: String!
    $attackVectorDescription: String!
    $compromisedAttributes: String
    $compromisedRecords: Int!
    $description: String!
    $findingId: String!
    $recommendation: String!
    $sorts: Sorts!
    $threat: String!
    $type: String
  ) {
    updateDescription(
      affectedSystems: $affectedSystems
      attackVectorDescription: $attackVectorDescription
      description: $description
      findingId: $findingId
      records: $compromisedAttributes
      recommendation: $recommendation
      recordsNumber: $compromisedRecords
      sorts: $sorts
      threat: $threat
      findingType: $type
    ) {
      success
    }
  }
`;

export { GET_FINDING_DESCRIPTION, UPDATE_DESCRIPTION_MUTATION };
