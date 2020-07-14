import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const PROJECTS_QUERY: DocumentNode = gql`
  query HomeProjects ($tagsField: Boolean!) {
    me(callerOrigin: "FRONT") {
      organizations {
        name
      }
      projects {
        name
        description
      }
      tags @include(if: $tagsField) {
        name
        projects {
          name
        }
      }
    }
  }
  `;
