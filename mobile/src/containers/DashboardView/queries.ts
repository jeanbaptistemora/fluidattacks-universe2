import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const PROJECTS_QUERY: DocumentNode = gql`{
  me {
    projects {
      closedVulnerabilities
      isCommunity
      openVulnerabilities
      serviceAttributes
    }
  }
}`;
