import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FINDING_DESCRIPTION: DocumentNode = gql`
  query GetFindingDescription(
    $canRetrieveAnalyst: Boolean!
    $canRetrieveSorts: Boolean!
    $findingId: String!
  ) {
    finding(identifier: $findingId) {
      actor
      affectedSystems
      attackVectorDescription
      compromisedAttributes
      compromisedRecords
      description
      hacker @include(if: $canRetrieveAnalyst)
      id
      openVulnerabilities
      recommendation
      requirements
      scenario
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
    $actor: String!
    $affectedSystems: String!
    $attackVectorDescription: String!
    $compromisedAttributes: String
    $compromisedRecords: Int!
    $description: String!
    $findingId: String!
    $recommendation: String!
    $requirements: String!
    $scenario: String!
    $sorts: Sorts!
    $threat: String!
    $title: String!
    $type: String
  ) {
    updateDescription(
      actor: $actor
      affectedSystems: $affectedSystems
      attackVectorDescription: $attackVectorDescription
      description: $description
      findingId: $findingId
      records: $compromisedAttributes
      recommendation: $recommendation
      recordsNumber: $compromisedRecords
      requirements: $requirements
      scenario: $scenario
      sorts: $sorts
      threat: $threat
      title: $title
      findingType: $type
    ) {
      success
    }
  }
`;

export { GET_FINDING_DESCRIPTION, UPDATE_DESCRIPTION_MUTATION };
