import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_TOE_LANGUAGES: DocumentNode = gql`
  query GetToeLanguages($groupName: String!) {
    group(groupName: $groupName) {
      name
      codeLanguages {
        language
        loc
      }
    }
  }
`;

export { GET_TOE_LANGUAGES };
