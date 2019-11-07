import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const PROJECTS_QUERY: DocumentNode = gql`
  query HomeProjects {
    me {
      projects {
        name
        description
      }
    }
  }
  `;
