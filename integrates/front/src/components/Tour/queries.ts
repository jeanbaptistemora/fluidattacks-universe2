import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const UPDATE_TOURS: DocumentNode = gql`
  mutation updateTours($newGroup: Boolean!, $newRoot: Boolean!) {
    updateTours(tours: { newGroup: $newGroup, newRoot: $newRoot }) {
      success
    }
  }
`;

export { UPDATE_TOURS };
