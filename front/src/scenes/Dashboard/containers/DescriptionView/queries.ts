import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_FINDING_DESCRIPTION: DocumentNode = gql`
  query GetFindingDescription($findingId: String!){
    finding(identifier: $findingId) {
      actor
      affectedSystems
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
