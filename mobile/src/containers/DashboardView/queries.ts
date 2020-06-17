import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GROUPS_QUERY: DocumentNode = gql`{
  me {
    groups: projects {
      closedVulnerabilities
      isCommunity
      openVulnerabilities
      serviceAttributes
    }
  }
}`;
