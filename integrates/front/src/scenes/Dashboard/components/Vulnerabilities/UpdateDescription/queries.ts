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

const DELETE_TAGS_MUTATION: DocumentNode = gql`
  mutation DeleteTagsVuln ($findingId: String!, $tag: String, $vulnerabilities: [String]!){
    deleteTags(findingId: $findingId, tag: $tag, vulnerabilities: $vulnerabilities) {
      success
    }
  }
`;

export { DELETE_TAGS_MUTATION, UPDATE_DESCRIPTION_MUTATION };
