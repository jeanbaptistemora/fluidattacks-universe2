import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_FINDING_DESCRIPTION: DocumentNode = gql`
  query GetFindingDescription(
    $canRetrieveAnalyst: Boolean!,
    $canEditTreatmentMgr: Boolean!,
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
      releaseDate
      remediated
      requirements
      risk
      scenario
      state
      title
      threat
      type
      verified
    }
    project(projectName: $projectName) {
      subscription
      users @include(if: $canEditTreatmentMgr) {
        email
      }
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
