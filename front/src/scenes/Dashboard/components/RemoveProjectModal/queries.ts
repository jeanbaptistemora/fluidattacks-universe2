import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const REMOVE_PROJECT_MUTATION: DocumentNode = gql`
  mutation RemoveProjectMutation(
    $projectName: String!,
    ) {
    removeProject(
      projectName: $projectName,
    ) {
      findingsMasked
      projectFinished
      success
      usersRemoved
    }
  }
`;
