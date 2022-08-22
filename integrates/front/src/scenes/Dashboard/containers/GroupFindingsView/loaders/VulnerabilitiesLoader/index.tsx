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
  const [treatmentAssignmentEmails, setTreatmentAssignmentEmails] =
    useState<string>("");
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
            treatmentAssignmentEmails,
            wheres,
          },
        })
      );
    }
  }, [findingId, setFindingVulnerabilities, treatmentAssignmentEmails, wheres]);

  if (
    _.isUndefined(pageInfo) ||
    (!_.isUndefined(pageInfo) && pageInfo.hasNextPage)
  ) {
    return <div />;
  }

  const newWheres = [
    ...new Set(
      vulnerabilities.map((value: IVulnerabilityAttr): string => value.where)
    ),
  ].join(", ");
  if (newWheres.length !== wheres.length) {
    setWheres(newWheres);
  }

  const newTreatmentAssignmentEmails = [
    ...new Set(
      vulnerabilities.map(
        (value: IVulnerabilityAttr): string | null => value.treatmentAssigned
      )
    ),
  ]
    .filter(
      (treatmentAssigned: string | null): boolean =>
        !_.isNull(treatmentAssigned)
    )
    .join(", ");
  if (
    newTreatmentAssignmentEmails.length !== treatmentAssignmentEmails.length
  ) {
    setTreatmentAssignmentEmails(newTreatmentAssignmentEmails);
  }

  return <div />;
};

export { VulnerabilitiesLoader };
