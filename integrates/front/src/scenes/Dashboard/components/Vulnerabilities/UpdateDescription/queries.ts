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

const REQUEST_ZERO_RISK_VULN: DocumentNode = gql`
mutation RequestZeroRiskVuln ($findingId: String!, $justification: String!, $vulnerabilities: [String]!){
  requestZeroRiskVuln(findingId: $findingId, justification: $justification, vulnerabilities: $vulnerabilities) {
    success
  }
}`;

export { DELETE_TAGS_MUTATION, REQUEST_ZERO_RISK_VULN, UPDATE_DESCRIPTION_MUTATION };
