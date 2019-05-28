import { gql } from "apollo-boost";
import { DocumentNode } from "graphql";

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
