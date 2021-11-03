import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const REMOVE_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation RemoveStakeholderMutation {
    removeStakeholder {
      success
    }
  }
`;
