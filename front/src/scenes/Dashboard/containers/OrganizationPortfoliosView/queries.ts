import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_USER_PORTFOLIOS: DocumentNode = gql`
  query GetUserPortfolios($allowed: Boolean!) {
    me(callerOrigin: "FRONT") {
      tags @include(if: $allowed) {
        name
        projects {
          name
        }
      }
    }
  }
`;
