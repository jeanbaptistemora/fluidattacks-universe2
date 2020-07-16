import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GROUPS_QUERY: DocumentNode = gql`{
  me {
    groups: projects {
      closedVulnerabilities
      openVulnerabilities
      serviceAttributes
    }
  }
}`;

export const ORGS_QUERY: DocumentNode = gql`{
  me {
    organizations {
      analytics(
        documentName: "remediation"
        documentType: "singleValueIndicator"
      )
      totalGroups
    }
  }
}`;
