import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import type { ColumnDef } from "@tanstack/react-table";
import { useFormikContext } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useEffect, useState } from "react";

import { GET_FINDING_VULNS_TO_REATTACK } from "./queries";
import type {
  IVulnerabilitiesConnection,
  IVulnerabilitiesToReattackTableProps,
  IVulnerabilityAttr,
  IVulnerabilityEdge,
} from "./types";

import type { IFormValues } from "../../AddModal";
import { Table as Tablez } from "components/Table";
import { Logger } from "utils/logger";

const VulnerabilitiesToReattackTable: React.FC<IVulnerabilitiesToReattackTableProps> =
  ({ finding }: IVulnerabilitiesToReattackTableProps): JSX.Element => {
    const { values, setFieldValue, setFieldTouched } =
      useFormikContext<IFormValues>();

    const { data, fetchMore } = useQuery<{
      finding: {
        vulnerabilitiesToReattackConnection:
          | IVulnerabilitiesConnection
          | undefined;
      };
    }>(GET_FINDING_VULNS_TO_REATTACK, {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          Logger.error("Couldn't load vulns to reattack", error);
        });
      },
      variables: {
        findingId: finding.id,
      },
    });
    const vulnsToReattackConnection =
      data === undefined
        ? undefined
        : data.finding.vulnerabilitiesToReattackConnection;
    const pageInfo =
      vulnsToReattackConnection === undefined
        ? undefined
        : vulnsToReattackConnection.pageInfo;
    const vulnsToReattackEdges: IVulnerabilityEdge[] =
      vulnsToReattackConnection === undefined
        ? []
        : vulnsToReattackConnection.edges;
    const vulnsToReattack: IVulnerabilityAttr[] = vulnsToReattackEdges.map(
      (vulnEdge: IVulnerabilityEdge): IVulnerabilityAttr => vulnEdge.node
    );

    const [selectedVulns, setSelectedVulns] = useState<IVulnerabilityAttr[]>(
      []
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

    const columnsz: ColumnDef<IVulnerabilityAttr>[] = [
      { accessorKey: "where", header: "Where" },
      { accessorKey: "specific", header: "Specific" },
    ];

    useEffect((): void => {
      setFieldTouched("affectedReattacks", true);
      const selectedIds = selectedVulns.map(
        (vuln): string => `${vuln.findingId} ${vuln.id}`
      );
      setFieldValue(
        "affectedReattacks",
        _.union(values.affectedReattacks, selectedIds)
      );
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [selectedVulns]);

    return (
      <Tablez
        columns={columnsz}
        data={vulnsToReattack}
        id={finding.id}
        rowSelectionSetter={setSelectedVulns}
        rowSelectionState={selectedVulns}
      />
    );
  };

export { VulnerabilitiesToReattackTable };
