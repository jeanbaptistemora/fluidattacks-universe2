import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_FINDING_TREATMENT: DocumentNode = gql`
  query GetFindingTreatment($findingId: String!) {
    finding(identifier: $findingId){
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
    $findingId: String!,
    $justification: String!,
    $treatment: UpdateClientDescriptionTreatment!
  ) {
    updateClientDescription(
      acceptanceDate: $date,
      acceptanceStatus: $acceptanceStatus,
      findingId: $findingId,
      justification: $justification,
      treatment: $treatment
    ) {
      success
    }
  }
  `;
