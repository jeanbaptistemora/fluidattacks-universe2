import { DocumentNode } from "graphql";
import gql from "graphql-tag";

const UPDATE_DESCRIPTION_MUTATION: DocumentNode = gql`
  mutation UpdateTreatmentVulnMutation(
    $findingId: String!,
    $severity: Int,
    $tag: String
    $treatmentManager: String,
    $vulnerabilities: [String]!,
    $externalBts: String!,
    $acceptanceDate: String,
    $justification: String!,
    $treatment: UpdateClientDescriptionTreatment!
    $isVulnTreatmentChanged: Boolean!,
    $isVulnInfoChanged: Boolean!,
  ) {
    updateTreatmentVuln (
      externalBts: $externalBts,
      findingId: $findingId,
      severity: $severity,
      tag: $tag,
      treatmentManager: $treatmentManager,
      vulnerabilities: $vulnerabilities,
    ) @include (if: $isVulnInfoChanged) {
      success
    }
    updateVulnsTreatment(
      acceptanceDate: $acceptanceDate,
      findingId: $findingId,
      justification: $justification,
      treatment: $treatment,
      treatmentManager: $treatmentManager,
      vulnerabilities: $vulnerabilities,
    ) @include (if: $isVulnTreatmentChanged) {
      success
    }
  }
`;

const DELETE_TAGS_MUTATION: DocumentNode = gql`
  mutation DeleteTagsVuln ($findingId: String!, $tag: String, $vulnerabilities: [String]!){
    deleteTags(findingId: $findingId, tag: $tag, vulnerabilities: $vulnerabilities) {
      success
    }
  }
`;

export { DELETE_TAGS_MUTATION, UPDATE_DESCRIPTION_MUTATION };
