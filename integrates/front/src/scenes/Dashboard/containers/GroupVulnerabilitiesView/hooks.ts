import type { ApolloQueryResult } from "@apollo/client";
import { useApolloClient, useQuery } from "@apollo/client";
import { useEffect, useState } from "react";

import { GET_FINDING_VULNERABILITIES, GET_GROUP_FINDINGS } from "./queries";
import type {
  IFindingVulnerabilities,
  IGroupFindings,
  IVulnerability,
} from "./types";

/*
 * [Experimental]
 * Retrieve paginated vulnerabilities from all group findings
 *
 * Using a bare apollo client instance as useQuery isn't flexible enough
 * to dynamically perform multiple queries
 */
const useGroupVulnerabilities = (groupName: string): IVulnerability[] => {
  const { data: findingsData } = useQuery<IGroupFindings>(GET_GROUP_FINDINGS, {
    variables: { groupName },
  });
  const [vulnerabilities, setVulnerabilities] = useState<IVulnerability[]>([]);
  const client = useApolloClient();

  useEffect((): (() => void) => {
    const findings =
      findingsData === undefined ? [] : findingsData.group.findings;

    const subscriptions = findings.map(
      (finding): ZenObservable.Subscription => {
        const observableQuery = client.watchQuery<IFindingVulnerabilities>({
          fetchPolicy: "cache-first",
          query: GET_FINDING_VULNERABILITIES,
          variables: { findingId: finding.id },
        });

        const onNext = ({
          data,
        }: ApolloQueryResult<IFindingVulnerabilities>): void => {
          const { edges, pageInfo } = data.finding.vulnerabilitiesConnection;
          const loadedVulnerabilities = edges.map(
            (edge): IVulnerability => edge.node
          );

          setVulnerabilities((currentValues): IVulnerability[] => [
            ...currentValues,
            ...loadedVulnerabilities,
          ]);

          if (pageInfo.hasNextPage) {
            void observableQuery.fetchMore({
              variables: { after: pageInfo.endCursor },
            });
          }
        };

        return observableQuery.subscribe(onNext);
      }
    );

    return (): void => {
      subscriptions.forEach((subscription): void => {
        subscription.unsubscribe();
      });
    };
  }, [client, findingsData]);

  return vulnerabilities;
};

export { useGroupVulnerabilities };
