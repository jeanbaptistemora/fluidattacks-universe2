import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const PROJECTS_QUERY: DocumentNode = gql`
  query HomeProjects ($tagsField: Boolean!) {
    me(callerOrigin: "FRONT") {
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
