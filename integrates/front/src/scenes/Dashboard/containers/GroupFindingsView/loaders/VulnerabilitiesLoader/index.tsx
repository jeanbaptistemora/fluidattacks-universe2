import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useEffect, useState } from "react";

import { GET_FINDING_LOCATIONS } from "./queries";
import type {
  IVulnerabilitiesConnection,
  IVulnerabilitiesLoaderProps,
  IVulnerabilitiesResume,
  IVulnerabilityAttr,
  IVulnerabilityEdge,
} from "./types";

import { Logger } from "utils/logger";

const VulnerabilitiesLoader: React.FC<IVulnerabilitiesLoaderProps> = ({
  findingId,
  setFindingVulnerabilities,
}): JSX.Element => {
  const [wheres, setWheres] = useState<string>("");
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
    if (!_.isEmpty(wheres)) {
      setFindingVulnerabilities(
        (
          prevState: Record<string, IVulnerabilitiesResume>
        ): Record<string, IVulnerabilitiesResume> => ({
          ...prevState,
          [findingId]: {
            assignments: wheres,
            wheres,
          },
        })
      );
    }
  }, [findingId, setFindingVulnerabilities, wheres]);

  if (
    _.isUndefined(pageInfo) ||
    (!_.isUndefined(pageInfo) && pageInfo.hasNextPage)
  ) {
    return <div />;
  }

  const newWheres = [
    ...new Set(
      vulnerabilities.map((value: { where: string }): string => value.where)
    ),
  ].join(", ");

  if (newWheres.length !== wheres.length) {
    setWheres(newWheres);
  }

  return <div />;
};

export { VulnerabilitiesLoader };
