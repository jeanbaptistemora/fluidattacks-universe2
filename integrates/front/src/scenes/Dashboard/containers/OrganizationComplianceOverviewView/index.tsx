/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";

import { GET_ORGANIZATION_COMPLIANCE } from "./queries";
import type {
  IComplianceAttr,
  IOrganizationComplianceOverviewProps,
} from "./types";

import { Col } from "components/Layout/Col";
import { Row } from "components/Layout/Row";
import { Logger } from "utils/logger";

const OrganizationComplianceOverviewView: React.FC<IOrganizationComplianceOverviewProps> =
  ({ organizationId }: IOrganizationComplianceOverviewProps): JSX.Element => {
    // GraphQl queries
    const { data } = useQuery<{
      organization: { compliance: IComplianceAttr };
    }>(GET_ORGANIZATION_COMPLIANCE, {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          Logger.error("Couldn't load organization compliance", error);
        });
      },
      variables: {
        organizationId,
      },
    });

    return (
      <React.StrictMode>
        <Row>
          <Col lg={60} md={60} sm={100}>
            <Row>
              <Col lg={33} md={33} sm={33}>
                {_.isUndefined(data) ? null : <div />}
              </Col>
            </Row>
          </Col>
          <Col lg={40} md={40} sm={100} />
        </Row>
      </React.StrictMode>
    );
  };

export { OrganizationComplianceOverviewView };
