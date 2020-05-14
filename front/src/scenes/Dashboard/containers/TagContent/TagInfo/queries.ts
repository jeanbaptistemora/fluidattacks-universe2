import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const TAG_QUERY: DocumentNode = gql`
  query GetTagInfo($tag: String!) {
    tag(tag: $tag) {
      lastClosingVuln
      maxOpenSeverity
      maxSeverity
      meanRemediateCriticalSeverity
      meanRemediateHighSeverity
      meanRemediateLowSeverity
      meanRemediateMediumSeverity
      meanRemediate
      name
      projects {
        closedVulnerabilities
        description
        lastClosingVuln
        maxOpenSeverity
        maxSeverity
        name
        openFindings
        openVulnerabilities
        totalFindings
        totalTreatment
      }
    }
  }
`;
