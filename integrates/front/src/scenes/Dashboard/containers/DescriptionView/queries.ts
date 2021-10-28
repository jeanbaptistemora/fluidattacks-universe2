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
      description
      hacker @include(if: $canRetrieveHacker)
      id
      openVulnerabilities
      recommendation
      releaseDate
      requirements
      sorts @include(if: $canRetrieveSorts)
      state
      threat
      title
    }
  }
`;

const GET_LANGUAGE: DocumentNode = gql`
  query GetLanguageQuery($groupName: String!) {
    group(groupName: $groupName) {
      name
      language
    }
  }
`;

const UPDATE_DESCRIPTION_MUTATION: DocumentNode = gql`
  mutation UpdateFindingDescription(
    $affectedSystems: String!
    $attackVectorDescription: String!
    $compromisedAttributes: String
    $description: String!
    $findingId: String!
    $recommendation: String!
    $sorts: Sorts!
    $threat: String!
    $title: String!
  ) {
    updateDescription(
      affectedSystems: $affectedSystems
      attackVectorDescription: $attackVectorDescription
      description: $description
      findingId: $findingId
      records: $compromisedAttributes
      recommendation: $recommendation
      sorts: $sorts
      threat: $threat
      title: $title
    ) {
      success
    }
  }
`;

export { GET_FINDING_DESCRIPTION, GET_LANGUAGE, UPDATE_DESCRIPTION_MUTATION };
