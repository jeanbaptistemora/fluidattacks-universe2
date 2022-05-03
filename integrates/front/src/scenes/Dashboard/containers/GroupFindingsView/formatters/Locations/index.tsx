import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useEffect } from "react";

import { GET_FINDING_LOCATIONS } from "./queries";
import type {
  ILocationsProps,
  IVulnerabilitiesConnection,
  IVulnerabilityAttr,
  IVulnerabilityEdge,
} from "./types";

import { limitFormatter } from "components/Table/formatters";
import { Logger } from "utils/logger";

const Locations: React.FC<ILocationsProps> = ({
  findingId,
  setFindingLocations,
}): JSX.Element => {
  const { data, fetchMore } = useQuery<{
    finding: {
      vulnerabilitiesConnection: IVulnerabilitiesConnection | undefined;
    };
  }>(GET_FINDING_LOCATIONS, {
    fetchPolicy: "cache-first",
    nextFetchPolicy: "cache-first",
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load finding locations", error);
      });
    },
    variables: {
      findingId,
    },
  });
  const vulnerabilitiesConnection =
    data === undefined ? undefined : data.finding.vulnerabilitiesConnection;
  const pageInfo =
    vulnerabilitiesConnection === undefined
      ? undefined
      : vulnerabilitiesConnection.pageInfo;
  const vulnerabilitiesEdges: IVulnerabilityEdge[] =
    vulnerabilitiesConnection === undefined
      ? []
      : vulnerabilitiesConnection.edges;
  const vulnerabilities: IVulnerabilityAttr[] = vulnerabilitiesEdges.map(
    (vulnerabilityEdge: IVulnerabilityEdge): IVulnerabilityAttr =>
      vulnerabilityEdge.node
  );

  const locations = vulnerabilities
    .map((value: { where: string }): string => value.where)
    .join(", ");

  useEffect((): void => {
    if (!_.isUndefined(pageInfo)) {
      if (pageInfo.hasNextPage) {
        void fetchMore({
          variables: { after: pageInfo.endCursor },
        });
      }
    }
  }, [findingId, vulnerabilities, pageInfo, fetchMore, setFindingLocations]);

  useEffect((): void => {
    if (locations.length > 0) {
      setFindingLocations(
        (prevState: Record<string, string>): Record<string, string> => ({
          ...prevState,
          [findingId]: locations,
        })
      );
    }
  }, [locations, findingId, setFindingLocations]);

  return limitFormatter(locations);
};

const locationsFormatter: (
  setFindingLocations: (
    setStateFn: (prevState: Record<string, string>) => Record<string, string>
  ) => void
) => (value: string) => JSX.Element = (
  setFindingLocations: (
    setStateFn: (prevState: Record<string, string>) => Record<string, string>
  ) => void
): ((value: string) => JSX.Element) => {
  const formatter: (value: string) => JSX.Element = (
    value: string
  ): JSX.Element => {
    return (
      <Locations findingId={value} setFindingLocations={setFindingLocations} />
    );
  };

  return formatter;
};

export { locationsFormatter };
