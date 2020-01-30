import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_FINDING_TREATMENT: DocumentNode = gql`
  query GetFindingTreatment($identifier: String!) {
    finding(identifier: $identifier){
      btsUrl
      historicTreatment
      id
    }
  }
`;

export const UPDATE_TREATMENT_MUTATION: DocumentNode = gql`
  mutation UpdateTreatmentMutation(
    $acceptanceDate: Date,
    $acceptanceStatus: String,
    $btsUrl: String,
    $findingId: String!,
    $justification: String,
    $treatment: String!
  ) {
    updateClientDescription(
      acceptanceDate: $acceptanceDate,
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
