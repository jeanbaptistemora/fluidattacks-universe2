import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const REMOVE_ACCOUNT_MUTATION: DocumentNode = gql`
  mutation RemoveAccountMutation {
    removeStakeholder {
      success
    }
  }
`;
