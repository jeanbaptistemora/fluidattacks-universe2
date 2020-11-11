import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_FINDING_DESCRIPTION: DocumentNode = gql`
  query GetFindingDescription(
    $canRetrieveAnalyst: Boolean!,
    $canRetrieveSorts: Boolean!,
    $findingId: String!
  ) {
    finding(identifier: $findingId) {
      actor
      affectedSystems
      analyst @include(if: $canRetrieveAnalyst)
      attackVectorDesc
      compromisedAttributes
      compromisedRecords
      cweUrl
      description
      historicTreatment
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

export const HANDLE_ACCEPTATION: DocumentNode = gql
  `mutation HandleAcceptation($findingId: String!, $observations: String!, $projectName: String!, $response: String!) {
    handleAcceptation(
      findingId: $findingId,
      observations: $observations,
      projectName: $projectName,
      response: $response
    ) {
      success
    }
  }`;

export const UPDATE_DESCRIPTION_MUTATION: DocumentNode = gql`
  mutation UpdateFindingDescription(
    $actor: String!,
    $affectedSystems: String!,
    $attackVectorDesc: String!,
    $compromisedAttributes: String,
    $compromisedRecords: Int!,
    $cweUrl: String!,
    $description: String!,
    $findingId: String!,
    $recommendation: String!,
    $requirements: String!,
    $scenario: String!,
    $sorts: Sorts!,
    $threat: String!,
    $title: String!,
    $type: String
  ){
    updateDescription(
      actor: $actor,
      affectedSystems: $affectedSystems,
      attackVectorDesc: $attackVectorDesc,
      cwe: $cweUrl,
      description: $description,
      findingId: $findingId,
      records: $compromisedAttributes,
      recommendation: $recommendation,
      recordsNumber: $compromisedRecords,
      requirements: $requirements,
      scenario: $scenario,
      sorts: $sorts,
      threat: $threat,
      title: $title,
      findingType: $type
    ) {
      success
    }
  }
`;
