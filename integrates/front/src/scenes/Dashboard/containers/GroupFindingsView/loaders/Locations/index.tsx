import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useEffect, useState } from "react";

import { GET_FINDING_LOCATIONS } from "./queries";
import type {
  ILocationsProps,
  IVulnerabilitiesConnection,
  IVulnerabilityAttr,
  IVulnerabilityEdge,
} from "./types";

import { Logger } from "utils/logger";

const Locations: React.FC<ILocationsProps> = ({
  findingId,
  setFindingLocations,
}): JSX.Element => {
  const [locations, setLocations] = useState<string>("");
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

  useEffect((): void => {
    if (!_.isUndefined(pageInfo)) {
      if (pageInfo.hasNextPage) {
        void fetchMore({
          variables: { after: pageInfo.endCursor },
        });
      }
    }
  }, [pageInfo, fetchMore]);

  useEffect((): void => {
    if (!_.isEmpty(locations)) {
      setFindingLocations(
        (prevState: Record<string, string>): Record<string, string> => ({
          ...prevState,
          [findingId]: locations,
        })
      );
    }
  }, [findingId, setFindingLocations, locations]);

  if (
    _.isUndefined(pageInfo) ||
    (!_.isUndefined(pageInfo) && pageInfo.hasNextPage)
  ) {
    return <div />;
  }

  const newLocations = [
    ...new Set(
      vulnerabilities.map((value: { where: string }): string => value.where)
    ),
  ].join(", ");

  if (newLocations.length !== locations.length) {
    setLocations(newLocations);
  }

  return <div />;
};

export { Locations };
