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
  ) {
    updateTreatmentVuln (
      externalBts: $externalBts,
      findingId: $findingId,
      severity: $severity,
      tag: $tag,
      treatmentManager: $treatmentManager,
      vulnerabilities: $vulnerabilities,
    ) {
      success
    }
  }
`;

export { UPDATE_DESCRIPTION_MUTATION };
