import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const REQUEST_REMOVE_PROJECT_MUTATION: DocumentNode = gql`
  mutation RequestRemoveProjectMutation(
    $projectName: String!,
    ) {
    requestRemoveProject(
      projectName: $projectName,
    ) {
      success
    }
  }
`;
