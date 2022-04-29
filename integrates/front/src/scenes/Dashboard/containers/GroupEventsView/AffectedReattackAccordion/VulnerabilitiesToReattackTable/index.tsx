import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import { useFormikContext } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useEffect } from "react";

import { GET_FINDING_VULNS_TO_REATTACK } from "./queries";
import type {
  IVulnerabilitiesConnection,
  IVulnerabilitiesToReattackTableProps,
  IVulnerabilityAttr,
  IVulnerabilityEdge,
} from "./types";

import type { IFormValues } from "../../AddModal";
import type { IReattackVuln } from "../types";
import { Table } from "components/Table";
import type { IHeaderConfig, ISelectRowProps } from "components/Table/types";
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

    useEffect((): void => {
      if (!_.isUndefined(pageInfo)) {
        if (pageInfo.hasNextPage) {
          void fetchMore({
            variables: { after: pageInfo.endCursor },
          });
        }
      }
    }, [pageInfo, fetchMore]);

    const columns: IHeaderConfig[] = [
      { dataField: "where", header: "Where" },
      { dataField: "specific", header: "Specific" },
    ];

    function onSelect(vuln: IReattackVuln, isSelected: boolean): void {
      setFieldTouched("affectedReattacks", true);
      const selectedId = `${vuln.findingId} ${vuln.id}`;
      if (isSelected) {
        setFieldValue(
          "affectedReattacks",
          _.union(values.affectedReattacks, [selectedId])
        );
      } else {
        setFieldValue(
          "affectedReattacks",
          values.affectedReattacks.filter(
            (item: string): boolean => item !== selectedId
          )
        );
      }
    }

    function onSelectAll(isSelected: boolean, vulns: IReattackVuln[]): void {
      setFieldTouched("affectedReattacks", true);
      const selectedIds = vulns.map(
        (vuln): string => `${vuln.findingId} ${vuln.id}`
      );
      if (isSelected) {
        setFieldValue(
          "affectedReattacks",
          _.union(values.affectedReattacks, selectedIds)
        );
      } else {
        setFieldValue(
          "affectedReattacks",
          values.affectedReattacks.filter(
            (identifier: string): boolean => !selectedIds.includes(identifier)
          )
        );
      }
    }

    const selectionMode: ISelectRowProps = {
      clickToSelect: true,
      mode: "checkbox",
      onSelect,
      onSelectAll,
    };

    return (
      <Table
        dataset={vulnsToReattack}
        exportCsv={false}
        headers={columns}
        id={finding.id}
        pageSize={10}
        rowSize={"thin"}
        search={false}
        selectionMode={selectionMode}
      />
    );
  };

export { VulnerabilitiesToReattackTable };
