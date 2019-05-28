import { DocumentNode, gql } from "apollo-boost";

export const PROJECTS_QUERY: DocumentNode = gql`query {
  me {
    projects {
      name
      description
    }
  }
}`;
