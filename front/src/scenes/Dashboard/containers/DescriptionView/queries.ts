import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_FINDING_DESCRIPTION: DocumentNode = gql`
  query GetFindingDescription(
    $canRetrieveAnalyst: Boolean!,
    $findingId: String!,
    $projectName: String!
  ) {
    finding(identifier: $findingId) {
      actor
      affectedSystems
      analyst @include(if: $canRetrieveAnalyst)
      attackVectorDesc
      btsUrl
      compromisedAttributes
      compromisedRecords
      cweUrl
      description
      historicTreatment
      id
      newRemediated
      openVulnerabilities
      recommendation
      requirements
      scenario
      state
      threat
      title
      type
      verified
    }
    project(projectName: $projectName) {
      subscription
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

export const VERIFY_FINDING: DocumentNode = gql`
  mutation VerifyFinding ($findingId: String!, $justification: String!) {
    verifyFinding(
      findingId: $findingId,
      justification: $justification
    ) {
      success
    }
  }
`;

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
      threat: $threat,
      title: $title,
      findingType: $type
    ) {
      success
    }
  }
`;
