import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_FINDING_TREATMENT: DocumentNode = gql`
  query GetFindingTreatment($findingId: String!) {
    finding(identifier: $findingId){
      btsUrl
      historicTreatment
      id
      openVulnerabilities
    }
  }
`;

export const UPDATE_TREATMENT_MUTATION: DocumentNode = gql`
  mutation UpdateTreatmentMutation(
    $date: String,
    $acceptanceStatus: String,
    $btsUrl: String,
    $findingId: String!,
    $justification: String!,
    $treatment: String!
  ) {
    updateClientDescription(
      acceptanceDate: $date,
      acceptanceStatus: $acceptanceStatus,
      btsUrl: $btsUrl,
      findingId: $findingId,
      justification: $justification,
      treatment: $treatment
    ) {
      success
    }
  }
  `;
